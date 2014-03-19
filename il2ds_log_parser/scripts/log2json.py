# -*- coding: utf-8 -*-
import optparse
import simplejson as json

from il2ds_log_parser import parse_log


def parse_args():
    usage = "usage: %prog --src=SRC --dst=DST"
    parser = optparse.OptionParser(usage)

    help = "Path to the source events log file. Default: events.log"
    parser.add_option('--src', default='events.log', help=help)

    help = "Path to the destination JSON file. Default: events.json"
    parser.add_option('--dst', default='events.json', help=help)

    options, args = parser.parse_args()
    return options.src, options.dst


def main():
    src, dst = parse_args()
    try:
        with open(src, 'r') as f:
            lines = [line.strip() for line in iter(f.readlines())]
    except IOError as e:
        print "Log reading error: {e}".format(e=e)
    else:
        missions, unparsed = parse_log(lines)

        count = min(30, len(unparsed))
        if count:
            print "First {count} skipped lines:".format(count=count)
            for line in unparsed[:count]:
                print line
        total = len(lines)
        skipped = len(unparsed)
        print "Total: {total}.\nDone: {done}.\nSkipped: {skipped}.".format(
            total=total, done=total-skipped, skipped=skipped)

        try:
            with open(dst, 'w') as f:
                json.dump(missions, f, sort_keys=True, indent=4 * ' ')
        except IOError as e:
            print "Result writing error: {e}".format(e=e)


if __name__ == '__main__':
    main()
