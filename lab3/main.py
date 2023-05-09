from argparse import ArgumentParser
from serializer import Serializer

if __name__ == '__main__':
    parser = ArgumentParser(description="Serializer JSON, XML")

    parser.add_argument("file_from", type=str, help="file from which you load data")
    parser.add_argument("file_to", type=str, help="file to which you save serialized data")
    parser.add_argument("format_from", type=str, help="format from which you deserialize data (json/xml)")
    parser.add_argument("format_to", type=str, help="format to which you serialize data (json/xml)")

    try:
        args = parser.parse_args()
        file_from = args.file_from
        file_to = args.file_to
        format_from = args.format_from
        format_to = args.format_to
    except SystemExit:
        file_from = "files/json_format.json"
        file_to = "files/xml_format.xml"
        format_from = "json"
        format_to = "xml"

    from_serializer = Serializer.create_serializer(format_from)
    to_serializer = Serializer.create_serializer(format_to)

    obj = from_serializer.load(file_from)
    print(f'Result = {obj}')
    to_serializer.dump(obj, file_to)