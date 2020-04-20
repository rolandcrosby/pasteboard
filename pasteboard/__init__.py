from AppKit import NSPasteboard
from CoreServices import UTTypeConformsTo
import argparse
import os
import sys
import errno
import tempfile
import subprocess
try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'wb')

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
                print(
                    "{}\tconforms to {}: {}".format(
                        t, args.type, UTTypeConformsTo(t, args.type)
                    )
                )
            else:
                print(t)


def type_for_args(args, pb):  # -> Optional[String]
    if args.type:
        return args.type
    ts = [uti for item in pb.pasteboardItems() for uti in item.types()]
    if len(ts) > 0:
        return ts[0]


def c_paste(args):
    pb = NSPasteboard.generalPasteboard()
    conforming_type = type_for_args(args, pb)
    if conforming_type is None:
        return
    data = data_conforming_to_type(pb, conforming_type)
    if data:
        if sys.version_info > (3, 0):
            sys.stdout.buffer.write(pb_bytes(data))
        else:
            sys.stdout.write(pb_bytes(data))
        return
    else:
        exit(errno.ENODATA)

def pb_bytes(data):
    if sys.version_info > (3, 0):
        return data[1].bytes()
    else:
        return data[1].bytes().tobytes()

def c_quicklook(args):
    pb = NSPasteboard.generalPasteboard()
    conforming_type = type_for_args(args, pb)
    if conforming_type is None:
        return
    data = data_conforming_to_type(pb, conforming_type)
    if data:
        tempdir = tempfile.mkdtemp()
        filename = os.path.join(tempdir, "clipboard")
        with open(filename, "wb") as f:
            f.write(pb_bytes(data))
        subprocess.call(
            ["/usr/bin/qlmanage", "-p", filename],
            stdout=DEVNULL,
            stderr=DEVNULL,
        )
        os.remove(filename)
        os.rmdir(tempdir)
    else:
        exit(errno.ENODATA)


def c_filter(args):
    pb = NSPasteboard.generalPasteboard()
    conforming_data = data_conforming_to_type(pb, args.type)
    if conforming_data:
        print(
            "{} conforms to {}, replacing clipboard contents".format(
                conforming_data[0], args.type
            )
        )
        pb.clearContents()
        pb.setData_forType_(conforming_data[1], conforming_data[0])
    else:
        exit(errno.ENODATA)


def main():
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers()

    sp_types = sp.add_parser("types", help="show available types")
    sp._name_parser_map["t"] = sp._name_parser_map["types"]
    sp_types.set_defaults(func=c_types)
    sp_types.add_argument("type", nargs="?", help="type to check for conformance with")

    sp_paste = sp.add_parser("paste", help="get contents of pasteboard")
    sp._name_parser_map["p"] = sp._name_parser_map["paste"]
    sp_paste.set_defaults(func=c_paste)
    sp_paste.add_argument("type", nargs="?", help="explicit type to request")

    sp_quicklook = sp.add_parser("quicklook", help="show the clipboard in Quick Look")
    sp._name_parser_map["ql"] = sp._name_parser_map["quicklook"]
    sp_quicklook.set_defaults(func=c_quicklook)
    sp_quicklook.add_argument("type", nargs="?", help="explicit type to request")

    sp_filter = sp.add_parser("filter", help="filter pasteboard to conforming types")
    sp._name_parser_map["f"] = sp._name_parser_map["filter"]
    sp_filter.set_defaults(func=c_filter)
    sp_filter.add_argument("type", help="type to filter for conformance")

    sp_image = sp.add_parser("image", help="filter pasteboard to public.image")
    sp._name_parser_map["im"] = sp._name_parser_map["image"]
    sp_image.set_defaults(
        func=lambda x: c_filter(argparse.Namespace(type="public.image"))
    )

    sp_text = sp.add_parser("text", help="filter pasteboard to public.plain-text")
    sp_text.set_defaults(
        func=lambda x: c_filter(argparse.Namespace(type="public.plain-text"))
    )

    args = parser.parse_args()
    if not "func" in args:
        parser.print_usage()
        return
    return args.func(args)


if __name__ == "__main__":
    main()
