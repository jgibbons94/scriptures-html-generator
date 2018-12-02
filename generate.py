#!/usr/bin/python3
import sqlite3, os, sys, shutil

#root output directory
root_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or os.path.dirname(__file__) or os.getcwd())
db_path = root_dir+"/lds-scriptures-sqlite3.db"
root_dir = root_dir+"/scriptures"
themes_dir=root_dir+"/themes"
menu_css_path=root_dir+"/menu.css"
scriptures_css_path=root_dir+"/scriptures.css"
main_menu_html_path=root_dir+"/main-menu.html"

if not os.path.exists(root_dir):
	os.mkdir(root_dir)

if not os.path.exists(themes_dir):
	os.mkdir(themes_dir)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def construct_volume(volume_row):
	"""construct the folder structure for a volume of scripture: bom, ot, nt, etc."""
	global root_dir
	global cursor
	global menu_css_path
	volume_dir=root_dir + "/" + volume_row[5]
	if not os.path.exists(volume_dir):
		os.mkdir(volume_dir)
	books = cursor.execute("select id, volume_id, book_title, book_long_title, book_subtitle, book_short_title, book_lds_url from books WHERE volume_id = %i" % volume_row[0]).fetchall()

	menu_path=volume_dir + "/menu.html"
	if not os.path.exists(menu_path):
		f = open(menu_path, "w", encoding="utf-8")
		f.write("""<!DOCTYPE html>
<html>
	<head>
		<link rel="stylesheet" href="{0}"> 
		<title>{1}</title>
	</head>
	<body class="center">
		<h1>{1}</h1>
		<pre>""".format(os.path.relpath(menu_css_path, start=os.path.dirname(menu_path)), volume_row[2]))
		for book in books:
			f.write("""
<a href="{0}/menu.html">{1}</a>""".format(book[6], book[2]))
		f.write("""
		</pre>
	</body>
</html>""")
		f.close()


	for book_row in books:
		construct_book(volume_row, book_row, volume_dir)

def construct_book(volume_row, book_row, volume_dir):
	"""construct the folder structure for a book of scripture: 1 Nephi, 2 Nephi, Jacob, etc."""
	global cursor
	global menu_css_path
	book_dir = volume_dir + "/" + book_row[6]
	menu_path = book_dir +"/menu.html"
	if not os.path.exists(book_dir):
		os.mkdir(book_dir)
	chapters = cursor.execute("select id, book_id, chapter_number FROM chapters WHERE book_id=%i"% book_row[0]).fetchall()
	if not os.path.exists(menu_path):
		f = open(menu_path, "w", encoding="utf-8")
		f.write("""<!DOCTYPE html>
<html>
	<head>
		<link rel="stylesheet" href="{0}"> 
		<title>{1}</title>
 </head>
	<body class="center">
		<h1>{1}</h1>
	<pre>""".format(os.path.relpath(menu_css_path, start=os.path.dirname(menu_path)),book_row[3]))
		for chapter in chapters:
			f.write("""
<a href="ch{0}.html">Chapter {0}</a>""".format(chapter[2]))
		f.write("""
		</pre>
	</body>
</html>
""")
		f.close()
	
	for chapter_row in chapters:
		construct_chapter(volume_row, book_row, chapter_row, book_dir)

def construct_chapter(volume_row, book_row, chapter_row, book_dir):
	"""construct the file for a chapter of scripture."""
	global cursor
	chapter_path = book_dir + "/ch" + str(chapter_row[2]) +".html"
	verses = cursor.execute("SELECT id, chapter_id, verse_number, scripture_text FROM verses WHERE chapter_id=%i" % chapter_row[0]).fetchall();
	if not os.path.exists(chapter_path):
		f = open(chapter_path, "w", encoding="utf-8")
		f.write("""<!DOCTYPE html>
<html>
	<head>
		<link rel="stylesheet" href="{0}"> 
		<title>{1} {2}</title>
	</head>
	<body>
		<h1>{3} Chapter {4}</h1>
		<ol class="{5} {6} ch{7}">
""".format(os.path.relpath(scriptures_css_path, start=os.path.dirname(chapter_path)), book_row[2], chapter_row[2], book_row[2], chapter_row[2], volume_row[5], book_row[6], chapter_row[2]))
		for verse in verses:
		#	print(verse[2], verse[3])
			f.write("""<li id="v{0}">
	<p>
		{1}
	</p>
</li>
""".format(verse[2], verse[3]))
		f.write("""			</ol>
	</body>
</html>
""")
		f.close()

night_menu_css_path = themes_dir + "/nightmenu.css"
if not os.path.exists(night_menu_css_path):
	f = open(night_menu_css_path, "w", encoding="utf-8")
	f.write("""html {
	font-family: sans;
	font-size: 150%;
	text-decoration: none;
	background: black;
	color: white;
}

a:link {
	font-family: sans;
	color: blue;
	text-decoration: none;
}

a:visited {
	font-family: sans;
	color: blue;
	text-decoration: none;
}

a:hover {
	font-family: sans;
	color: blue;
	font-weight: bold;
	font-size: 110%;
	text-decoration: none;
}

a:active {
	font-family: sans;
	color: blue;
	font-weight: bold;
	font-size: 110%;
	text-decoration: none;
}

.center {
	text-align: center;
}
""")
	f.close()

night_scriptures_css_path = themes_dir + "/nightscriptures.css"
if not os.path.exists(night_scriptures_css_path):
	f = open(night_scriptures_css_path, "w", encoding="utf-8")
	f.write("""html {
	background: black;
}

p {
	font-size: 110%;
	font: sans, serif, monospace;
	color: white;
}

.first {
	font-size: 150%;
}

b {
	font-size: 70%;
}

h1 {
	text-align: center;
	color: white;
}

table {
	border-collapse: separate;
	border-spacing: 5px;
	margin: 0 auto;
}

th, td { 
	padding: 10px;
	color: white;
}

a:hover {
	color: white;
	text-decoration: none;
}

ol li p{
font-weight:500;
color:white;
}
ol li{
font-weight:700;
color:white;
}
""")
	f.close()

normal_menu_css_path = themes_dir + "/normalmenu.css"
if not os.path.exists(normal_menu_css_path):
	f = open(normal_menu_css_path, "w", encoding="utf-8")
	f.write("""html {
	font-family: sans;
	font-size: 150%;
	text-decoration: none;
	background: white;
	color: black;
}

a:link {
	font-family: sans;
	color: blue;
	text-decoration: none;
}

a:visited {
	font-family: sans;
	color: blue;
	text-decoration: none;
}

a:hover {
	font-family: sans;
	color: blue;
	font-weight: bold;
	font-size: 110%;
	text-decoration: none;
}

a:active {
	font-family: sans;
	color: blue;
	font-weight: bold;
	font-size: 110%;
	text-decoration: none;
}

.center {
	text-align: center;
}
""")
	f.close()

normal_scriptures_css_path = themes_dir + "/normalscriptures.css"
if not os.path.exists(normal_scriptures_css_path):
	f = open(normal_scriptures_css_path, "w", encoding="utf-8")
	f.write("""html {
	background: white;
}

p {
	font-size: 110%;
	font: sans, serif, monospace;
	color: black;
}

.first {
	font-size: 150%;
}

b {
	font-size: 70%;
}

h1 {
	text-align: center;
	color: black;
}

table {
	border-collapse: separate;
	border-spacing: 5px;
	margin: 0 auto;
}

th, td { 
	padding: 10px;
	color: black;
}

a:hover {
	color: white;
	text-decoration: none;
}
ol li p{
font-weight:500;
color:black;
}
ol li{
font-weight:700;
color:black;
}
""")
	f.close()




if not os.path.exists(menu_css_path):
	shutil.copy(normal_menu_css_path, menu_css_path)

if not os.path.exists(scriptures_css_path):
	shutil.copy(normal_scriptures_css_path, scriptures_css_path)

volumes = cursor.execute('SELECT id, volume_title, volume_long_title, volume_title, volume_short_title, volume_lds_url FROM volumes').fetchall()
#Write all the necessary shared files: menu and css files

if not os.path.exists(main_menu_html_path):
	f = open(main_menu_html_path, "w", encoding="utf-8")
	f.write("""<!DOCTYPE html>
<html>
	<head>
		<link rel="stylesheet" href="./menu.css"> 
		<title>Standard Works</title>
	 </head>
		<body class="center">
			<h1>Library</h1>
		<pre>
""")
	for volume in volumes:
		f.write("""<a href='{0}/menu.html'>{1}</a>
""".format(volume[5], volume[2]))
	f.write("""<a href="http://www.lds.org">LDS.org</a>
		</pre>
	</body>
</html>
""")
	f.close()

for row in volumes:
	construct_volume(row)
print("done.")
