from glob import glob

if __name__ == '__main__':
    scores = []
    for f in glob('D:/SynologyDrive/2019_FA/MUS_105/Species/*.musicxml'):
        print(f)