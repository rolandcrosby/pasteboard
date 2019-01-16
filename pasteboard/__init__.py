from __future__ import print_function
from AppKit import NSPasteboard
from CoreServices import UTTypeConformsTo
import argparse
import sys
import errno

def data_conforming_to_type(pasteboard, uti):
    for item in pasteboard.pasteboardItems():
        ts = item.types()
        for t in ts:
            if UTTypeConformsTo(t, uti):
                return (t, item.dataForType_(t))

def c_types(args):
    for item in NSPasteboard.generalPasteboard().pasteboardItems():
        ts = item.types()
        for t in ts:
            if args.type:
                print("{}\tconforms to {}: {}".format(t, args.type, UTTypeConformsTo(t, args.type)))
            else:
                print(t)

def c_paste(args):
    pb = NSPasteboard.generalPasteboard()
    if args.type:
        t = args.type
    else:
        ts = [uti for item in pb.pasteboardItems() for uti in item.types()]
        if len(ts) > 0:
            t = ts[0]
        else:
            return
    data = data_conforming_to_type(pb, t)
    if data:
        if sys.version_info > (3, 0):
            sys.stdout.buffer.write(data[1].bytes())
        else:
            sys.stdout.write(data[1].bytes().tobytes())
        return
    else:
        exit(errno.ENODATA)

def c_filter(args):
    pb = NSPasteboard.generalPasteboard()
    conforming_data = data_conforming_to_type(pb, args.type)
    if conforming_data:
        print("{} conforms to {}, replacing clipboard contents".format(conforming_data[0], args.type))
        pb.clearContents()
        pb.setData_forType_(conforming_data[1], conforming_data[0])
    else:
        exit(errno.ENODATA)

def main():
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers()

    sp_types = sp.add_parser('types', help='show available types')
    sp_types.set_defaults(func=c_types)
    sp_types.add_argument('type', nargs='?', help="type to check for conformance with")
    
    sp_paste = sp.add_parser('paste', help='get contents of pasteboard')
    sp_paste.set_defaults(func=c_paste)
    sp_paste.add_argument('type', nargs='?', help="explicit type to request")

    sp_filter = sp.add_parser('filter', help='filter pasteboard to conforming types')
    sp_filter.set_defaults(func=c_filter)
    sp_filter.add_argument('type', help='type to filter for conformance')
    
    if sys.version_info > (3, 0):
        sp._name_parser_map['t'] = sp._name_parser_map['types']
        sp._name_parser_map['p'] = sp._name_parser_map['paste']
        sp._name_parser_map['f'] = sp._name_parser_map['filter']

    args = parser.parse_args()
    if not 'func' in args:
        parser.print_usage()
        return
    return args.func(args)

if __name__ == "__main__":
    main()
