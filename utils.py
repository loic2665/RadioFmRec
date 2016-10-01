def add_tuples(tup1, tup2):
	ls1 = list(tup1)
	ls2 = list(tup2)
	ls = [x + y for x, y in zip(tup1, tup2)]
	tup = tuple(ls)
	return tup

def substract_tuples(tup1, tup2):
	ls1 = list(tup1)
	ls2 = list(tup2)
	ls = [x - y for x, y in zip(tup1, tup2)]
	tup = tuple(ls)
	return tup

def getSongName(song_path):
	pathLs = song_path.split("/")
	fileNameLs = pathLs[-1].split(".")
	songName = fileNameLs[0]
	return songName
