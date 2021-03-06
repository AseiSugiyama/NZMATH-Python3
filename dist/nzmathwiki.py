"""
This program creates manual for NZMATH from NZMATH wiki.
"""

from HTMLParser import HTMLParser
import datetime
import os
import sys
import urllib
import urlparse
import htmlentitydefs
import nzmath.compatibility

#------ global variable

# base url
basepla = 'nzmath.sourceforge.net'
basewiki = '/wiki/'
basedoc = '/doc/'
HPpla = 'tnt.math.metro-u.ac.jp'
HPdoc = '/nzmath/'

# normal option
ad_list = set(['UserManual']) # start page's list
del_list = set(['', 'FrontPage', 'OtherProjects', 'BracketName', 'InterWikiName', 'References']) # not use as local file
up_list = set(['UserManual', 'Install', 'Tutorial', 'FAQ']) # not module page
ja_flag = False # japanese manual
p_out = True # output intermediate steps
sleeptime = 1 # sleep time
retry = 5 # web retry number

# for japanese up_list
if ja_flag:
    up_list =  set(list(up_list) + [x+'.ja' for x in up_list])


#------ utility function
def back_to_tag(tag, attrs):
    """
    recover tag from tag name and attributes.
    """
    sol = '<' + tag
    for (prop, val) in attrs:
        sol += ' ' + prop + '="' + val + '"'
    sol += '>'
    return sol

def getHeader(files):
    """
    create header
    """
    head = '<div id="header">' + '\n'
    head += ' <h1 class="title">'
    head += '<a href="'
    head += convertDocURL(files)
    #head += '">?' + urllib.unquote(files) + '</a></h1>' + '\n'
    head += '">' + urllib.unquote(files) + '</a></h1>' + '\n'
    head += '</div>' + '\n'
    return head

def getFooter():
    """
    create footer
    """
    foot = '<div id="footer">' + '\n'
    foot += ' Copyright &copy; 2003-' + str(datetime.datetime.today().year) + ', '
    foot += '<a href="'
    foot += convertHPURL('')
    foot += '">' + 'NZMATH</a> deveropment group' + '\n'
    foot += '</div>' + '\n'
    return foot

def convertFileName(url):
    """
    convert url to local file name.(FileNameToFile is essential)
    """
    split_url = urlparse.urlparse(url)
    try:
        if split_url[1] == basepla:
            if split_url[4] in del_list:
                raise InputError
            elif split_url[4][:8] == 'cmd=edit':
                raise InputError
            else:
                sol = FileNameToFile(str(split_url[4]))
                if not(ja_flag) and '.ja.html' in sol:
                    raise InputError
            return (sol, split_url[5], split_url[4])
        else:
            raise InputError
    except InputError:
        return url.replace('&', '&amp;')

def FileNameToFile(files):
    """
    convert url to file name essentially.
    """
    files = files.replace('%20%28ja%29', '.ja')
    if files in up_list:
        if  files == 'UserManual':
            return "index.html"
        elif files == 'UserManual.ja':
            return "index.ja.html"
        else:
            return files.lower() + ".html"
    else: # modules
        sol = files.replace('.py', '').replace('%2F', '_')
        return 'modules/' + sol + '.html'

def convertWikiURL(files):
    """
    convert file to wiki address.
    """
    return urlparse.urlunsplit( ('http', basepla, basewiki, files, '') )

def convertWikiHPURL(files):
    """
    convert file to wiki address (but not wiki form).
    """
    return urlparse.urlunsplit( ('http', basepla, basewiki + files, '', '') )

def convertDocURL(files):
    """
    convert file to document(manual address) address.
    """
    return urlparse.urlunsplit( ('http', basepla, basedoc, files, '') )

def convertHPURL(files):
    """
    convert file to NZMATH homepage address.
    """
    return urlparse.urlunsplit( ('http', HPpla, HPdoc + files, '', '') )

def convertEntity(data):
    """
    convert 2byte character to HTML entity. 
    """
    txt = unicode(str(data), 'euc_jp')
    sol = u''
    for char in txt:
        num = ord(char)
        if num > 127:
            try:
                sol += '&' + htmlentitydefs.codepoint2name[num] + ';'
            except:
                sol += char
        else:
            sol += char
    return sol.encode('euc_jp')

def retryConnection(func, *args, **kw):
    """
    retry connection to web.
    """
    try_num = 0
    while True:
        try:
            web_file = func(*args, **kw)
            break
        except IOError:
            try_num += 1
            if try_num >= retry:
                raise IOError
            if p_out:
                print "retry connection..."
            os.system('sleep ' +  str(sleeptime))
    return web_file

#------ Error Class
class NoneOutput(Exception):
    """
    Exception class for no output(simillar to GoTo statement)
    """
    pass

class InputError(Exception):
    """
    for Input Exception
    """
    pass

#------ create modified html
class MyWikiParser(HTMLParser):
    """
    create modified html(main module)
    """
    def __init__(self, files):
        self.files = files
        self.url = convertDocURL(files)
        conv = convertFileName(self.url)[0]
        if conv.find('modules/') == -1:
            self.up = True
        else:
            self.up = False
        self.f = file(conv, 'w')
        if p_out:
            print "make from " + self.url
        self.deal = False
        HTMLParser.__init__(self)

    def handle_data(self, data):
        if not(self.deal):
            p_data = data.replace('This is a currently developing', 'This is a released')
            p_data = convertEntity(p_data.replace('- NZMATHWiki', '- NZMATH'))
            self.f.write(p_data)

    def handle_starttag(self, tag, attrs):
        if not(self.deal):
            try:
                p_attrs = attrs
                if tag == 'div':
                    if attrs:
                        if attrs[0][0] == 'id':
                            if attrs[0][1] == 'footer':
                                self.deal = 'div'
                                self.f.write(getFooter())
                                raise NoneOutput
                            if attrs[0][1] == 'header':
                                self.deal = 'div'
                                self.f.write(getHeader(self.files))
                                raise NoneOutput
                            if attrs[0][1] == 'lastmodified':
                                self.deal = 'div'
                                raise NoneOutput
                        if attrs[0][0] == 'class':
                            if attrs[0][1] == 'jumpmenu':
                                self.deal = 'div'
                                raise NoneOutput
                if tag == 'a':
                    if attrs[0][0] == 'href':
                        f_name = convertFileName(attrs[0][1])
                        if isinstance(f_name, tuple):
                            p_f_name = f_name[0]
                            if not(self.up):
                                if p_f_name.find('modules/') == -1:
                                    p_f_name = '../' + p_f_name
                                else:
                                    p_f_name = p_f_name[8:]
                            if f_name[1] != '':
                                p_attrs[0] = (attrs[0][0], p_f_name +
                                              '#' + f_name[1])
                            else:
                                p_attrs[0] = (attrs[0][0], p_f_name)
                            if not(os.path.exists(f_name[0])):
                                ad_list.add(f_name[2])
                        else:
                            p_attrs[0] = (attrs[0][0], f_name)
                    if attrs[0][0] == 'class':
                        if attrs[0][1] == 'anchor_super':
                            del p_attrs[3]
                            del p_attrs[2]
                self.f.write(back_to_tag(tag, p_attrs))
            except NoneOutput:
                pass

    def handle_endtag(self, tag):
        if not(self.deal):
            self.f.write('</' + tag + '>')
        if self.deal == tag:
            self.deal = False

    def handle_startendtag(self, tag, attrs):
        if not(self.deal):
            try:
                p_attrs = list(attrs)
                if tag == 'link':
                    if attrs[0][0] == 'rel':
                        if attrs[1][0] == 'href':
                            if self.up:
                                p_attrs[1] = (attrs[1][0], 'default.css')
                            else:
                                p_attrs[1] = (attrs[1][0], '../default.css')
                if tag == 'img':
                    #raise NoneOutput
                    if attrs[1][0] == 'src':
                        parse = urlparse.urlparse(attrs[1][0])
                        if parse[0] == '':
                            imgpage = convertWikiHPURL(self.files + attrs[1][1])
                            imgfile = attrs[1][1]
                        else:
                            imgpage = attrs[1][1]
                            imgfile = parse[2]
                        if p_out:
                            print "get img from " + imgpage
                        retryConnection(urllib.urlretrieve, imgpage, imgname)
                self.f.write(back_to_tag(tag, p_attrs)[:-1] + ' />')
            except NoneOutput:
                pass

    def handle_charref(self, ref):
        if not(self.deal):
            self.f.write('&#' + ref + ';')

    def handle_entityref(self, name):
        if not(self.deal):
            self.f.write('&' + name + ';')

    def handle_comment(self, data):
        if not(self.deal):
            self.f.write('<!--' + data + '-->')

    def handle_decl(self, decl):
        if not(self.deal):
            self.f.write('<!' + decl + '>')

    def handle_pi(self, data):
        if not(self.deal):
            self.f.write('<?' + data + '>')

    def close(self):
        self.f.close()
        HTMLParser.close(self)

    def feeds(self):
        HTMLParser.feed(self, retryConnection(urllib.urlopen, self.url).read())

#------ preparation
def main(base_path):
    """
    preparation for creating files.
    """
    current = os.getcwd()
    try:
        if not(os.path.exists(base_path)):
            ans = 'y'
            if p_out:
                print "Do you want to create " + base_path + "?(y/n)"
                ans = sys.stdin.read(1)
                print ""
            if ans in ('y', 'Y'):
                pass
            elif ans in ('n', 'N'):
                raise NoneOutput
            else:
                raise InputError
        else:
            m_path = os.path.join(base_path, 'nzmath/manual')
            if os.path.exists(m_path):
                ans = 'y'
                if p_out:
                    print "Do you want to remove " + m_path + "?(y/n)"
                    ans = sys.stdin.read(1)
                    print ""
                if ans in ('y', 'Y'):
                    for root, dirs, files in os.walk(m_path, topdown=False):
                        for name in files:
                            os.remove(os.path.join(root, name))
                        for name in dirs:
                            os.rmdir(os.path.join(root, name))
                elif ans in ('n', 'N'):
                    raise NoneOutput
                else:
                    raise InputError
        dirname = os.path.join(base_path, 'nzmath/manual/modules')
        if not(os.path.exists(dirname)):
            os.makedirs(dirname)
        os.chdir(os.path.join(base_path, 'nzmath/manual/'))
        csspage = convertHPURL('manual/default.css')
        if p_out:
            print "get css from " + csspage
        retryConnection(urllib.urlretrieve, csspage, 'default.css')
        while ad_list:
            files = ad_list.pop()
            MyWikiParser(files).feeds()
        if p_out:
            print "\n" + "All process is done!" + "\n"
            print "Ok, now created nzmath-current manual located to"
            print os.path.join(base_path, "nzmath")
            print "if you check difference between nzmath-cvs manual, with GNU diff,"
            print "$ diff -ubBr /tmp/nzmath/manual {your-nzmathcvs-repo}/manual"
            print "or you check only new version files,"
            print "$ diff -r --brief /tmp/nzmath/manual {your-nzmathcvs-repo}/manual ."
    except NoneOutput:
        if p_out:
            print 'end.'
    except InputError:
        print "Error: Invalid input!"
    except LookupError:
        print "Error: Maybe, Japanese encodings(ex.euc_jp) is not supported."
    except:
        if p_out:
            print "Check " + base_path + " (dir? truly path? and so on.)"
            print "Delete " + base_path + " and try again."
            print "(Maybe, caused by problem of network connection)\n"
        print sys.exc_info()[0]
    os.chdir(current)

#------ start!
if __name__ == '__main__':
    basepath = './tmp'
    if len( sys.argv) > 1:
        basepath = sys.argv[1]

    main(basepath)
