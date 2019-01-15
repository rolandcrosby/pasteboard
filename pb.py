from __future__ import print_function
from AppKit import NSPasteboard
from CoreServices import UTTypeConformsTo
import argparse
import sys

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
        sys.stdout.buffer.write(data[1].bytes())
        return

def c_filter(args):
    pb = NSPasteboard.generalPasteboard()
    conforming_data = data_conforming_to_type(pb, args.type)
    if conforming_data:
        print("{} conforms to {}, replacing clipboard contents".format(conforming_data[0], args.type))
        pb.clearContents()
        pb.setData_forType_(conforming_data[1], conforming_data[0])

def main():
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers()

    sp_types = sp.add_parser('types', aliases=['t'], help='show available types')
    sp_types.set_defaults(func=c_types)
    sp_types.add_argument('type', nargs='?', help="type to check for conformance with")
    
    sp_paste = sp.add_parser('paste', aliases=['p'], help='get contents of pasteboard')
    sp_paste.set_defaults(func=c_paste)
    sp_paste.add_argument('type', nargs='?', help="explicit type to request")

    sp_filter = sp.add_parser('filter', aliases=['f'], help='filter pasteboard to conforming types')
    sp_filter.set_defaults(func=c_filter)
    sp_filter.add_argument('type', help='type to filter for conformance')
    
    args = parser.parse_args()
    if not 'func' in args:
        parser.print_usage()
        return
    return args.func(args)

if __name__ == "__main__":
    main()
