from flask import Flask, render_template, request, redirect
import datetime

app = Flask(__name__)

@app.route("/")
def homepage():

	try:
		f = open("tasks.txt", "r")
	except IOError:
		os.system("touch tasks.txt")
		f = open("tasks.txt", "r")

	try:
		cal = open("cal.txt", "r")
	except IOError:
		os.system("touch cal.txt")
		cal = open("cal.txt", "r")

	try:
		dia = open("dairy.txt", "r")
	except IOError:
		os.system("touch dairy.txt")
		dia = open("dairy.txt", "r")

	f = f.read()

	f = f.split(".")
	# events = [list(i.split(',')) for i in cal]

	events = []
	for i in cal:
		a = i.split(',')
		events.append([int(a[0]), int(a[1]), a[2]])


	Diary = []
	for i in dia:
		if ":-" in i:
			i = i.split(":-")
		Diary.append(i)

	dia = []
	for i in range(len(Diary) - 1, -1, -2):
		dia.append(Diary[i - 1])
		dia.append(Diary[i])

	events.sort(key = lambda row:(row[1],row[0]))

	imp = [w[:len(w) - 1] for w in f if w.endswith('@')]
	f = [w for w in f if not w.endswith('@')]

	return render_template("index.html", tasks = f, imp = imp, events = events, diary = dia)

@app.route("/addtask", methods = ["POST"])
def addtask():
	task = request.form['newtask']
	
	f = open("tasks.txt", "a")
	
	f.write("." + task)
	f.close()

	return redirect("/")

@app.route("/addcalevent", methods = ["POST"])
def addcalevent():

	cal = open("cal.txt", "a")

	date = request.form['date']
	month = request.form['month']
	event = request.form['event']

	cal.write(date + ", " + month + ", " + event + "\n")

	return redirect("/")

@app.route("/del/<task>")
def delete(task):

	f = open("tasks.txt", "r")
	f = f.read()
	tasks = f.split(".")

	tasks.remove(task)
	# f.close()

	f = open("tasks.txt", "w")
	f.write(".".join(tasks))
	f.close()

	return redirect("/")

@app.route("/adddiary",methods = ['POST'])
def diary():

	dia = open("dairy.txt", 'a')
	now = str(datetime.datetime.now())
	# now = ""

	tag = request.form['tag']
	today = request.form['today']

	dia.write(now + "\n" + tag + ":- " + today + "\n")
	dia.close()

	return redirect("/")

if __name__ == "__main__":
	app.run(debug = True)