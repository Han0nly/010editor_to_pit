import pfp
import os
import sys
import subprocess
import random
from optparse import OptionParser

GlobalNumber =1;
PRINT_STRING_LIMIT = 8

INTENT_CHAR ="  "
def MutateInt(size):
    return  random.randint(0, pow(2,size));


def MutateString(instr=1024*"A"):
    p = subprocess.Popen("radamsa -n 1",stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.stdin.write(instr)
    text = p.communicate()[0]
    return text

def GeneratePit(src, template):
    dom = None

    dom = pfp.parse(data_file=src, template_file=template)

    ppit("DateModel",dom)
    '''
    for elem in png._pfp__children:
        try:
            print type(elem)
        except Exception,e :
            print e
            pass
    '''

def isAsciiStr(str):
    for c in str:
        if c < '\x20':
            return False
    return True


def hasChildren(Elem):
    try:
        p = Elem._pfp__children
        return True;
    except:
        return False;

def isArray(Elem):
    if isinstance(Elem, pfp.fields.Array):
        return True
    return False

def isUByte(Elem):
    if isinstance(Elem, pfp.fields.UChar) or isinstance(Elem, pfp.fields.Char):
        return True
    return False;

def isUint(Elem):
    if isinstance(Elem, pfp.fields.UInt):
        return True
    return False

def isUshort(Elem):
    if isinstance(Elem, pfp.fields.UShort) or isinstance(Elem, pfp.fields.WChar) or isinstance(Elem, pfp.fields.WUChar) :
        return True
    return False

def isUint64(Elem):
    if isinstance(Elem, pfp.fields.UInt64):
        return True
    return False;
def isUnion(Elem):
    if isinstance(Elem, pfp.fields.Union):
        return True
    return False

def isStruct(Elem):
    if isinstance(Elem, pfp.fields.Struct):
        return True
    else:
        return False;

def isString(Elem):
    if isinstance(Elem, pfp.fields.String):
        return True
    else:
        return False;

def isWString(Elem):
    if isinstance(Elem, pfp.fields.WString):
        return True
    else:
        return False;
def isEnum(Elem):
    if isinstance(Elem, pfp.fields.Enum):
        return True
    else:
        return False;


def ParseDom(Depth, Elem):
    try:
        name =""
        if isinstance(Elem, pfp.fields.Char):
            return;

        if Elem._pfp__name is not None:
            name = Elem._pfp__name
        else:
            name = "CHUNK"

        print "++"*Depth + name
        if hasChildren(Elem):
            [ParseDom(Depth+1, child) for child in Elem._pfp__children]

        if isArray(Elem):
            [ParseDom(Depth+1, e) for e in Elem]

    except Exception, e:
        print "*********"
        print  Elem
        print "*********"
        pass

def ppit(DataName, Dom):
    print '<?xml version="1.0" encoding="utf-8"?>'
    print '<Peach version="1.0" author="MJX" >'
    print '<DataModel name="%s">' % DataName

    pp(2, Dom)

    print '</DataModel>'
    print '</Peach>'



def pp(Depth, Elem):
    global GlobalNumber
    try:
        name = ""

        if Elem._pfp__name is not None:
            name = Elem._pfp__name
        else:
            name = "CHUNK%d" % GlobalNumber
            GlobalNumber +=1

        #print "++"*Depth + name, Elem

        if isUnion(Elem):
            print INTENT_CHAR*Depth,
            print '<Choice name="%s" minOccurs="1" maxOccurs="1">' % name, "<!--Union-->"
            [pp(Depth+1, child) for child in Elem._pfp__children]
            print INTENT_CHAR*Depth,
            print '</Choice>'
        elif isStruct(Elem):

            print INTENT_CHAR*Depth, '<Block name="%s">' % name
            [pp(Depth+1, child) for child in Elem._pfp__children]
            print INTENT_CHAR*Depth, '</Block>'

        elif isArray(Elem):
            if len(Elem) >0 and isinstance(Elem[0], pfp.fields.UChar):
                print INTENT_CHAR*Depth,
                print PrintBlobPit(name), "<!--UCHAR-->"
            elif len(Elem) >0 and isinstance(Elem[0], pfp.fields.Char):
                print INTENT_CHAR*Depth,
                print PrintStringPit(name, len(Elem), pfp.fields.get_str(Elem)), "<!--CHAR-->"
            else:
                print INTENT_CHAR*Depth,
                print '<Block name="%s">' % name
                [pp(Depth+1, e) for e in Elem]
                print INTENT_CHAR*Depth,
                print '</Block>'
        elif isUint(Elem):
            print INTENT_CHAR*Depth, PrintNumberPit(name, 32, Elem._pfp__value) ,'<!--int -->'
        elif isUshort(Elem):
            print INTENT_CHAR*Depth,PrintNumberPit(name, 16, Elem._pfp__value)
        elif isUint64(Elem):
            print INTENT_CHAR*Depth, PrintNumberPit(name, 64, Elem._pfp__value)
        elif isUByte(Elem):
            print INTENT_CHAR*Depth,PrintNumberPit(name, 8, Elem._pfp__value)
        elif isEnum(Elem):
            print INTENT_CHAR*Depth,PrintNumberPit(name, 4*Elem.width, Elem._pfp__value)," <!--enum-->"

        else:
            print INTENT_CHAR*Depth,PrintUnknown(name), "<!--", Elem, "-->"

    except Exception, e:
        print "*********"
        print  Elem
        print e
        print "*********"
        pass


def PrintUnknown(name):
    return '<Unkown name = "%s"/>' % name

def PrintNumberPit(name, size, value=None):
    #if value is not None:
    #    return '<Number name="%s"  valueType = "hex" size="%d" value="%x"/>' % (name, size, value)
    #else:
    return '<Number name="%s" size="%d"/>' % (name, size)


def PrintStringPit(name, length = 0, value=None):
    if value is None or len(value) > PRINT_STRING_LIMIT :
        return '<String name="%s" length="%d"/>' % (name, length)
    if not isAsciiStr(value):
        return '<String name="%s" length="%d"/>' % (name, length)
    return '<String name="%s" length="%d" value="%s"/>' % (name, length, value)

def PrintBlobPit(name):
    return '<Blob name="%s"/>' % name

def PrintBlockPit(name, data):
    s =  '<Block name=%s>' % name
    s += data
    s += '</Block>'

if __name__ == "__main__":
    MSG_USAGE = ""
    optParser = OptionParser(MSG_USAGE)
    #optParser.add_option("-f","--file",action = "store",type="string",dest = "fileName")
    #optParser.add_option("-v","--vison", action="store_false", dest="verbose",default='gggggg', help="make lots of noise [default]")
    optParser.add_option("-f","--file",action = "store",type="string",dest = "fileName")
    optParser.add_option("-t","--template",action = "store",type="string",dest = "template")
    options, args = optParser.parse_args()

    #print options.fileName
    #print options.template
    #print options.fileName
    #print MutateString()
    GeneratePit(options.fileName, options.template)
