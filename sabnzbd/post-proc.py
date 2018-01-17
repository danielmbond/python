#! python3
import os, requests, shutil, subprocess, sys, urllib.request, zipfile

if 'APPDATA' in os.environ:
    ffmpeg = os.path.join(os.environ['APPDATA'], 'ffmpeg', 'ffmpeg.exe')
else:
    ffmpeg = os.path.join(os.environ['HOME'], 'ffmpeg', 'ffmpeg.exe')

#Unzip file
def unzip(file):
    zip_ref = zipfile.ZipFile(file, 'r')
    zip_ref.extractall(os.path.dirname(os.path.realpath(file)))
    zip_ref.close()

#Convert files to MP4 
def convertToMp4(file, ffmpeg=ffmpeg):
    mp4 = os.path.join(os.path.splitext(file)[0] + ".mp4")
    subprocess.call([ffmpeg, "-i", file, "-c:v", "libx264", "-preset", "medium", "-shortest", mp4, '-loglevel', 'quiet'])

def plexScan():
    sections = (1,2,5,6)
    for i in sections:
        url = "http://127.0.0.1:32400/library/sections/" + str(i) + "/refresh?force=1&X-Plex-Token=yAqjrc2Ef1aza1j9fZ2x"
        r = requests.get(url)

#Download fmpeg if it's not around
def getFFMPEG(path=ffmpeg):
    if not os.path.isfile(path):
        ffmpegBaseDir = os.path.dirname(os.path.realpath(path))
        if not os.path.isdir(ffmpegBaseDir):
            os.makedirs(ffmpegBaseDir)
        ffmpegZip = os.path.join(ffmpegBaseDir, 'ffmpeg-latest-win64-static.zip')
        if not os.path.isfile(ffmpegZip):
            url = 'http://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-latest-win64-static.zip'
            request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(request) as response, open(ffmpegZip, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        unzip(ffmpegZip)
        ffmpeg = os.path.join(ffmpegBaseDir, r'ffmpeg-latest-win64-static\bin\ffmpeg.exe')
        os.rename(ffmpeg, os.path.join(ffmpegBaseDir, 'ffmpeg.exe'))
        os.remove(ffmpegZip)
        shutil.rmtree(os.path.join(ffmpegBaseDir, r'ffmpeg-latest-win64-static'))

def processMovieFiles(directory):
    movies = []
    for file in os.listdir(directory):
        fileFullname = os.path.join(directory, file)
        fileSize = os.path.getsize(fileFullname)
        print(fileSize)
        if (file.endswith(".mkv") or file.endswith(".avi") or file.endswith(".mpg")) and (fileSize > 10000000):
            movies.append(fileFullname)
            print("Converting", file)
        elif file.endswith("mp4") or file.endswith("m4v"):
            os.utime(fileFullname)
            print(file, "is already an MP4")
    for movie in movies:
        convertToMp4(movie)
        os.remove(movie)

try:
    getFFMPEG()
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        processMovieFiles(directory)
        plexScan()
except Exception as e:
    print('Exception: ', e)

