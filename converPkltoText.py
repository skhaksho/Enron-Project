import cPickle

words = cPickle.load(open("D:\Data\enron_emails_all_words.pkl", "r"))

thefile = open('D:\Data\EnronEmailText.txt', 'w')

for item in words:
  thefile.write(str(item).replace("(u'","").replace("'","").replace(")","") + "\n")

thefile.close()
