import numpy as np
import ffmpeg
import random
import json
import os

def getTimestamps(path: os.PathLike, fileType: str='json3'):
  return json.load(open(path))['events']

def zoo(timestamps: [], path: os.PathLike): 
  for item in timestamps:
    stream = ffmpeg.input(path)
    stream = ffmpeg.output(stream,
      f"./output/{random.random() * 20239}_{random.random() * 2039}.ar.wav", 
      **{'ss': f"{item['tStartMs']}ms", 't': f"{item['dDurationMs']}ms", 'ac': 1, 'ar': 22050}
    )
    ffmpeg.run(stream)

def buildSubtitleAudioDict(listFiles: [str], fileType: str='json3'):
  out_dict = {}
  if(len(listFiles) != 2):
    raise Exception(f"listFiles must be of lenth of 2 but found {len(listFiles)}")
  for file in listFiles:
    if(file.endswith(fileType)):
      out_dict['subtitle'] = file
    else:
      out_dict['audio'] = file
  return out_dict

  
def getNestedSubtitleAndAudioFilesPath(path: str,suffix: str='webm', backList: list=[]):
  for x in os.scandir(path):
    if(x.is_file() and x.name.endswith(suffix)):
      backList.append(buildSubtitleAudioDict([os.path.join(path, file) for file in os.listdir(path)]))
      return
    if(x.is_dir()):
      getNestedSubtitleAndAudioFilesPath(x.path, suffix, backList)
  return backList

if __name__ == '__main__':
  for item in getNestedSubtitleAndAudioFilesPath(os.getcwd()):
    print(item['audio'])
    zoo(getTimestamps(item['subtitle']), item['audio'])
    break