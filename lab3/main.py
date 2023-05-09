from argparse import ArgumentParser
from serializer import Serializer

if __name__ == '__main__':
    parser = ArgumentParser(description="Serializer JSON, XML")

    parser.add_argument("file_from", type=str, help="file from which you load data")
    parser.add_argument("file_to", type=str, help="file to which you save serialized data")
    parser.add_argument("format_from", type=str, help="format from which you deserialize data (json/xml)")
    parser.add_argument("format_to", type=str, help="format to which you serialize data (json/xml)")

    args = parser.parse_args()

    try:
        serializer = Serializer.create_serializer("json")
        config = serializer.load("files/config_file.txt")

        file_from = config.get("file_from", args.file_from)
        file_to = config.get("file_to", args.file_to)
        format_from = config.get("format_from", args.format_from)
        format_to = config.ger("format_to", args.format_to)
    except FileNotFoundError:
        file_from = args.file_from
        file_to = args.file_to
        format_from = args.format_from
        format_to = args.format_to

    from_serializer = Serializer.create_serializer(format_from)
    to_serializer = Serializer.create_serializer(format_to)

    obj = from_serializer.load(file_from, format_from)
    print(f'Result = \n{obj}')
    to_serializer.dump(obj, format_to)