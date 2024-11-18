# -*- coding: utf-8 -*-
"""voice_morph

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1n2wepb58fd_BuZuMajuc1lhYYjsFZPIU
"""

# Commented out IPython magic to ensure Python compatibility.
#@title  **Main Step: INSTALL  THE MODEL**
# %cd /content
from IPython.display import clear_output
from ipywidgets import Button
import subprocess, shlex, os
from google.colab import drive

var = "We"+"bU"+"I"
test = "Voice"
c_word = "Conversion"
r_word = "Retrieval"
#!git clone https://github.com/RVC-Project/{r_word}-based-{test}-{c_word}-{var} /content/RVC
!git clone https://github.com/splendormagic/RVC_BahaaMahmoud /content/RVC

!pip install pip==24.0

!apt -y install -qq aria2
pretrains = ["f0D32k.pth","f0G32k.pth"]
new_pretrains = ["f0Ov2Super32kD.pth","f0Ov2Super32kG.pth"]

for file in pretrains:
    if not os.path.exists(f"/content/RVC/assets/pretrained_v2/{file}"):
        command = "aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/%s%s%s/resolve/main/pretrained_v2/%s -d /content/RVC/assets/pretrained_v2 -o %s" % ("Voice","Conversion","WebUI",file,file)
        try:
            subprocess.run(shlex.split(command))
        except Exception as e:
            print(e)

for file in new_pretrains:
    if not os.path.exists(f"/content/RVC/assets/pretrained_v2/{file}"):
        command = "aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/poiqazwsx/Ov2Super32kfix/resolve/main/%s -d /content/RVC/assets/pretrained_v2 -o %s" % (file,file)
        try:
            subprocess.run(shlex.split(command))
            print(shlex.split(command))
        except Exception as e:
            print(e)

!mkdir -p /content/dataset && mkdir -p /content/RVC/audios
!wget -nc https://raw.githubusercontent.com/RejektsAI/EasyTools/main/original -O /content/RVC/original.py
!wget -nc https://raw.githubusercontent.com/RejektsAI/EasyTools/main/app.py -O /content/RVC/demo.py
!wget -nc https://raw.githubusercontent.com/RejektsAI/EasyTools/main/easyfuncs.py -O /content/RVC/easyfuncs.py
!wget -nc https://huggingface.co/Rejekts/project/resolve/main/download_files.py -O /content/RVC/download_files.py
!wget -nc https://huggingface.co/Rejekts/project/resolve/main/a.png -O /content/RVC/a.png
!wget -nc https://huggingface.co/Rejekts/project/resolve/main/easy_sync.py -O /content/RVC/easy_sync.py
!wget -nc https://huggingface.co/spaces/Rejekts/RVC_PlayGround/raw/main/app.py -O /content/RVC/playground.py
!wget -nc https://huggingface.co/spaces/Rejekts/RVC_PlayGround/raw/main/tools/useftools.py -O /content/RVC/tools/useftools.py
!wget -nc https://huggingface.co/Rejekts/project/resolve/main/astronauts.mp3 -O /content/RVC/audios/astronauts.mp3
!wget -nc https://huggingface.co/Rejekts/project/resolve/main/somegirl.mp3 -O /content/RVC/audios/somegirl.mp3
!wget -nc https://huggingface.co/Rejekts/project/resolve/main/someguy.mp3 -O /content/RVC/audios/someguy.mp3
!wget -nc https://huggingface.co/Rejekts/project/resolve/main/unchico.mp3 -O /content/RVC/audios/unchico.mp3
!wget -nc https://huggingface.co/Rejekts/project/resolve/main/unachica.mp3 -O /content/RVC/audios/unachica.mp3
!cd /content/RVC && python /content/RVC/download_files.py

if not "installed" in locals():
    !cd /content/RVC && pip install -r requirements.txt
    !pip install mega.py gdown==5.1.0 pytube pydub  gradio==3.42.0
installed=True

#save_to_drive=True#@param {type:"boolean"}
save_to_drive=False

if save_to_drive:
    try:
        from google.colab import auth
        from pydrive2.auth import GoogleAuth
        from oauth2client.client import GoogleCredentials
        from pydrive2.drive import GoogleDrive
        auth.authenticate_user()
        gauth = GoogleAuth()
        gauth.credentials = GoogleCredentials.get_application_default()
        my_drive = GoogleDrive(gauth)
        drive.mount('/content/drive')
        drive_trash = my_drive.ListFile({'q': "trashed = true"}).GetList()
        from RVC.easy_sync import GarbageMan
        kevin = GarbageMan()
        kevin.start(path=drive_trash,every=40,pattern="[GD]_*.pth")
    except Exception as e:
        print(e)
from RVC.easy_sync import Channel
logs_folder ='/content/drive/MyDrive/project-main/logs'
weights_folder = '/content/drive/MyDrive/project-main/assets/weights'
if not "logs_backup" in locals(): logs_backup = Channel('/content/RVC/logs',logs_folder,every=30,exclude="mute")
if not "weights_backup" in locals(): weights_backup = Channel('/content/RVC/assets/weights',weights_folder,every=30)

if os.path.exists('/content/drive/MyDrive'):
    if not os.path.exists(logs_folder): os.makedirs(logs_folder)
    if not os.path.exists(weights_folder): os.makedirs(weights_folder)
    logs_backup.start()
    weights_backup.start()

clear_output()
Button(description="\u2714 Success", button_style="success")

"""---

**Training  Models**
"""

#@title **Step 1:** Upload Dataset (the vocals)
#@markdown Upload one clean vocal audio file. **( Recommended : 3 - 7 minutes clean vocal audio file)**
import os
from IPython.display import Audio
from IPython.core.display import display

upload_method = 'Upload' #@param ['Upload']

if not os.path.exists('/content/dataset'):
    os.makedirs('/content/dataset')

#remove previous input audio
if os.path.isfile('/content/dataset/vocal_audio.wav'):
    os.remove('/content/dataset/vocal_audio.wav')

def displayAudio():
  display(Audio('/content/dataset/vocal_audio.wav'))


if upload_method == 'Upload':
  from google.colab import files
  uploaded = files.upload()
  for fn in uploaded.keys():
    print('User uploaded file "{name}" with length {length} bytes.'.format(
        name=fn, length=len(uploaded[fn])))

  # Consider only the first file
  PATH_TO_YOUR_AUDIO = str(list(uploaded.keys())[0])

  # Load audio with specified sampling rate
  import librosa
  audio, sr = librosa.load(PATH_TO_YOUR_AUDIO, sr=None)

  # Save audio with specified sampling rate
  import soundfile as sf
  sf.write('/content/dataset/vocal_audio.wav', audio, sr, format='wav')

print("DONE.")

# Commented out IPython magic to ensure Python compatibility.
#@title **Step 2 :** Create Training Files
import os
from pytube import YouTube
from IPython.display import clear_output

def calculate_audio_duration(file_path):
    duration_seconds = len(AudioSegment.from_file(file_path)) / 1000.0
    return duration_seconds

def youtube_to_wav(url,dataset_folder="/content/dataset"):
    try:
        yt = YouTube(url).streams.get_audio_only().download(output_path=dataset_folder)
        mp4_path = os.path.join(dataset_folder,'audio.mp4')
        wav_path = os.path.join(dataset_folder,'audio.wav')
        os.rename(yt,mp4_path)
        !ffmpeg -i {mp4_path} -acodec pcm_s16le -ar 44100 {wav_path}
        os.remove(mp4_path)
    except Exception as e:
        print(e)

# %cd /content/RVC
#@markdown  Model name must be in English. Don't use "Spaces" or "Symbols".

#@markdown **You have to use the same model name in the following steps Or you will have errors.**

model_name = 'ntkav' #@param {type:"string"}
#dataset_folder = '/content/dataset' #@param {type:"string"}
dataset_folder = '/content/dataset'

#or_paste_a_youtube_link=""#@param {type:"string"}
or_paste_a_youtube_link=""
if or_paste_a_youtube_link !="":
    youtube_to_wav(or_paste_a_youtube_link)

from pydub import AudioSegment
file_path = dataset_folder
try:
    duration = calculate_audio_duration(file_path)
    if duration < 600:
        cache = True
    else:
        cache = False
except:
    cache = False

while len(os.listdir(dataset_folder)) < 1:
    input("Your dataset folder is empty.")
!mkdir -p ./logs/{model_name}
with open(f'./logs/{model_name}/preprocess.log','w') as f:
    print("Starting...")
!python infer/modules/train/preprocess.py {dataset_folder} 32000 2 ./logs/{model_name} False 3.0 > /dev/null 2>&1
with open(f'./logs/{model_name}/preprocess.log','r') as f:
    if 'end preprocess' in f.read():
        clear_output()
        display(Button(description="\u2714 Success", button_style="success"))
    else:
        print("Error preprocessing data... Make sure your dataset folder is correct.")

f0method = "rmvpe_gpu" # @param ["pm", "harvest", "rmvpe", "rmvpe_gpu"]
# %cd /content/RVC
with open(f'./logs/{model_name}/extract_f0_feature.log','w') as f:
    print("Starting...")
if f0method != "rmvpe_gpu":
    !python infer/modules/train/extract/extract_f0_print.py ./logs/{model_name} 2 {f0method}
else:
    !python infer/modules/train/extract/extract_f0_rmvpe.py 1 0 0 ./logs/{model_name} True
#!python infer/modules/train/extract_feature_print.py cuda:0 1 0 0 ./logs/{model_name} v2
!python infer/modules/train/extract_feature_print.py cuda:0 1 0 ./logs/{model_name} v2 True
with open(f'./logs/{model_name}/extract_f0_feature.log','r') as f:
    if 'all-feature-done' in f.read():
        clear_output()
    else:
        print("Error preprocessing data... Make sure your data was preprocessed.")
import numpy as np
import faiss
# %cd /content/RVC
def train_index(exp_dir1, version19):
    exp_dir = "logs/%s" % (exp_dir1)
    os.makedirs(exp_dir, exist_ok=True)
    feature_dir = (
        "%s/3_feature256" % (exp_dir)
        if version19 == "v1"
        else "%s/3_feature768" % (exp_dir)
    )
    if not os.path.exists(feature_dir):
        return "请先进行特征提取!"
    listdir_res = list(os.listdir(feature_dir))
    if len(listdir_res) == 0:
        return "请先进行特征提取！"
    infos = []
    npys = []
    for name in sorted(listdir_res):
        phone = np.load("%s/%s" % (feature_dir, name))
        npys.append(phone)
    big_npy = np.concatenate(npys, 0)
    big_npy_idx = np.arange(big_npy.shape[0])
    np.random.shuffle(big_npy_idx)
    big_npy = big_npy[big_npy_idx]
    if big_npy.shape[0] > 2e5:
        infos.append("Trying doing kmeans %s shape to 10k centers." % big_npy.shape[0])
        yield "\n".join(infos)
        try:
            big_npy = (
                MiniBatchKMeans(
                    n_clusters=10000,
                    verbose=True,
                    batch_size=256 * config.n_cpu,
                    compute_labels=False,
                    init="random",
                )
                .fit(big_npy)
                .cluster_centers_
            )
        except:
            info = traceback.format_exc()
            logger.info(info)
            infos.append(info)
            yield "\n".join(infos)

    np.save("%s/total_fea.npy" % exp_dir, big_npy)
    n_ivf = min(int(16 * np.sqrt(big_npy.shape[0])), big_npy.shape[0] // 39)
    infos.append("%s,%s" % (big_npy.shape, n_ivf))
    yield "\n".join(infos)
    index = faiss.index_factory(256 if version19 == "v1" else 768, "IVF%s,Flat" % n_ivf)
    infos.append("training")
    yield "\n".join(infos)
    index_ivf = faiss.extract_index_ivf(index)  #
    index_ivf.nprobe = 1
    index.train(big_npy)
    faiss.write_index(
        index,
        "%s/trained_IVF%s_Flat_nprobe_%s_%s_%s.index"
#         % (exp_dir, n_ivf, index_ivf.nprobe, exp_dir1, version19),
    )

    infos.append("adding")
    yield "\n".join(infos)
    batch_size_add = 8192
    for i in range(0, big_npy.shape[0], batch_size_add):
        index.add(big_npy[i : i + batch_size_add])
    faiss.write_index(
        index,
        "%s/added_IVF%s_Flat_nprobe_%s_%s_%s.index"
#         % (exp_dir, n_ivf, index_ivf.nprobe, exp_dir1, version19),
    )
    infos.append(
        "成功构建索引，added_IVF%s_Flat_nprobe_%s_%s_%s.index"
#         % (n_ivf, index_ivf.nprobe, exp_dir1, version19)
    )

training_log = train_index(model_name, 'v2')

for line in training_log:
    print(line)
    if 'adding' in line:
        clear_output()
        display(Button(description="\u2714 Success", button_style="success"))

# Commented out IPython magic to ensure Python compatibility.
#@title **Step 3 :** Training Model
# %cd /content/RVC
from random import shuffle
import json
import os
import pathlib
from subprocess import Popen, PIPE, STDOUT
now_dir=os.getcwd()

#@markdown  Enter the name of your model again. It must be **THE SAME YOU CHOSE ABOVE**
model_name = 'ntkav'#@param {type:"string"}
#@markdown ---


#@markdown  The "epochs" value is how much you would like to train you model. **(Recommended : 200 - 1000)**

epochs = 2000 # @param {type:"slider", min:50, max:2000, step:10}

#@markdown ---

#@markdown  Saving frequency during the training. **(Recommended : 50)**

save_frequency = 50 # @param {type:"slider", min:10, max:100, step:10}
#save_frequency = 20

##@markdown ---
##@markdown <small> **Advanced Settings**:

# Remove the logging setup
#OV2=True#@param {type:"boolean"}
OV2=True

#batch_size = 8 # @param {type:"slider", min:1, max:20, step:1}
batch_size = 8
sample_rate='32k'
if OV2:
    G_file=f'assets/pretrained_v2/f0Ov2Super{sample_rate}G.pth'
    D_file=f'assets/pretrained_v2/f0Ov2Super{sample_rate}D.pth'
else:
    G_file=f'assets/pretrained_v2/f0G{sample_rate}.pth'
    D_file=f'assets/pretrained_v2/f0D{sample_rate}.pth'
def click_train(
    exp_dir1,
    sr2,
    if_f0_3,
    spk_id5,
    save_epoch10,
    total_epoch11,
    batch_size12,
    if_save_latest13,
    pretrained_G14,
    pretrained_D15,
    gpus16,
    if_cache_gpu17,
    if_save_every_weights18,
    version19,
):
    # 生成filelist
    exp_dir = "%s/logs/%s" % (now_dir, exp_dir1)
    os.makedirs(exp_dir, exist_ok=True)
    gt_wavs_dir = "%s/0_gt_wavs" % (exp_dir)
    feature_dir = (
        "%s/3_feature256" % (exp_dir)
        if version19 == "v1"
        else "%s/3_feature768" % (exp_dir)
    )
    if if_f0_3:
        f0_dir = "%s/2a_f0" % (exp_dir)
        f0nsf_dir = "%s/2b-f0nsf" % (exp_dir)
        names = (
            set([name.split(".")[0] for name in os.listdir(gt_wavs_dir)])
            & set([name.split(".")[0] for name in os.listdir(feature_dir)])
            & set([name.split(".")[0] for name in os.listdir(f0_dir)])
            & set([name.split(".")[0] for name in os.listdir(f0nsf_dir)])
        )
    else:
        names = set([name.split(".")[0] for name in os.listdir(gt_wavs_dir)]) & set(
            [name.split(".")[0] for name in os.listdir(feature_dir)]
        )
    opt = []
    for name in names:
        if if_f0_3:
            opt.append(
                "%s/%s.wav|%s/%s.npy|%s/%s.wav.npy|%s/%s.wav.npy|%s"
#                 % (
                    gt_wavs_dir.replace("\\", "\\\\"),
                    name,
                    feature_dir.replace("\\", "\\\\"),
                    name,
                    f0_dir.replace("\\", "\\\\"),
                    name,
                    f0nsf_dir.replace("\\", "\\\\"),
                    name,
                    spk_id5,
                )
            )
        else:
            opt.append(
                "%s/%s.wav|%s/%s.npy|%s"
#                 % (
                    gt_wavs_dir.replace("\\", "\\\\"),
                    name,
                    feature_dir.replace("\\", "\\\\"),
                    name,
                    spk_id5,
                )
            )
    fea_dim = 256 if version19 == "v1" else 768
    if if_f0_3:
        for _ in range(2):
            opt.append(
                "%s/logs/mute/0_gt_wavs/mute%s.wav|%s/logs/mute/3_feature%s/mute.npy|%s/logs/mute/2a_f0/mute.wav.npy|%s/logs/mute/2b-f0nsf/mute.wav.npy|%s"
#                 % (now_dir, sr2, now_dir, fea_dim, now_dir, now_dir, spk_id5)
            )
    else:
        for _ in range(2):
            opt.append(
                "%s/logs/mute/0_gt_wavs/mute%s.wav|%s/logs/mute/3_feature%s/mute.npy|%s"
#                 % (now_dir, sr2, now_dir, fea_dim, spk_id5)
            )
    shuffle(opt)
    with open("%s/filelist.txt" % exp_dir, "w") as f:
        f.write("\n".join(opt))

    # Replace logger.debug, logger.info with print statements
    print("Write filelist done")
    print("Use gpus:", str(gpus16))
    if pretrained_G14 == "":
        print("No pretrained Generator")
    if pretrained_D15 == "":
        print("No pretrained Discriminator")
    if version19 == "v1" or sr2 == "40k":
        config_path = "configs/v1/%s.json" % sr2
    else:
        config_path = "configs/v2/%s.json" % sr2
    config_save_path = os.path.join(exp_dir, "config.json")
    if not pathlib.Path(config_save_path).exists():
        with open(config_save_path, "w", encoding="utf-8") as f:
            with open(config_path, "r") as config_file:
                config_data = json.load(config_file)
                json.dump(
                    config_data,
                    f,
                    ensure_ascii=False,
                    indent=4,
                    sort_keys=True,
                )
            f.write("\n")

    cmd = (
        'python infer/modules/train/train.py -e "%s" -sr %s -f0 %s -bs %s -g %s -te %s -se %s %s %s -l %s -c %s -sw %s -v %s'
#         % (
            exp_dir1,
            sr2,
            1 if if_f0_3 else 0,
            batch_size12,
            gpus16,
            total_epoch11,
            save_epoch10,
            "-pg %s" % pretrained_G14 if pretrained_G14 != "" else "",
            "-pd %s" % pretrained_D15 if pretrained_D15 != "" else "",
            1 if if_save_latest13 == True else 0,
            1 if if_cache_gpu17 == True else 0,
            1 if if_save_every_weights18 == True else 0,
            version19,
        )
    )
    # Use PIPE to capture the output and error streams
    p = Popen(cmd, shell=True, cwd=now_dir, stdout=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True)

    # Print the command's output as it runs
    for line in p.stdout:
        print(line.strip())

    # Wait for the process to finish
    p.wait()
    return "训练结束, 您可查看控制台训练日志或实验文件夹下的train.log"
# %load_ext tensorboard
# %tensorboard --logdir ./logs --port=8888
if "cache" not in locals():
    cache = False
training_log = click_train(
    model_name,
    sample_rate,
    True,
    0,
    save_frequency,
    epochs,
    batch_size,
    True,
    G_file,
    D_file,
    0,
    cache,
    True,
    'v2',
)
print(training_log)

"""---

**Backup & Loading Models**
"""

#@title **Backup Model To Google Drive**

#@markdown  Enter the same exact name of the model you trained.

import os

if not os.path.exists('/content/RVC'):
  print("You need to run the first cell before loading your model! Run the GUI, stop it and then load the model.")
else:
  Model_Name = "ntkav"#@param {type:"string"}
  folder = Model_Name
  Type = "Save" #@param ["Save"]
  import tarfile, os
  from google.colab import drive
  drive.mount('/content/drive')
  !mkdir -p /content/drive/MyDrive/RVC_Packages
  if Type=='Save':
    with tarfile.open(f'/content/drive/MyDrive/RVC_Packages/{folder}.tar.gz','w:gz') as tar:
      tar.add(f'/content/RVC/logs/{folder}', arcname=f'logs/{folder}')
      if os.path.exists(f'/content/RVC/assets/weights/{folder}.pth'):
        tar.add(f'/content/RVC/assets/weights/{folder}.pth', arcname=f'assets/weights/{folder}.pth')
      print(f'Backed up {folder} to RVC_Packages in your google drive.')
  else:
    if not os.path.exists(f'/content/drive/MyDrive/RVC_Packages/{folder}.tar.gz'):
      print("File not found.")
    else:
      with tarfile.open(f'/content/drive/MyDrive/RVC_Packages/{folder}.tar.gz','r:gz') as tar:
        tar.extractall('/content/RVC')

#@title **Load Model From Google Drive**


!pip install --upgrade --no-cache-dir gdown
import tarfile

#@markdown  Enter the same exact name of the model you want to load.

Model_Name = "ntspb"#@param {type:"string"}

#@markdown _Paste the link of (.tar.gz) file from Google Drive and Remember to make it public link._

model_pth_name = Model_Name + ".tar.gz"

MODEL_LINK = "https://drive.google.com/file/d/1-A8rR8Ii8FcREK-Bb5Q16ggtlgT9Y7zD/view?usp=drive_link" #@param {type:"string"}

if MODEL_LINK != "":
  pth = '/content/sample_data/'

  dwnld = pth + model_pth_name
  print('[1;32mDownload model...')
  !gdown --fuzzy -O $dwnld "$MODEL_LINK"
  #clear_output()
  print('[1;32mDone!')
else:
  print('[1;31mPaste model link and try again!')

if not os.path.exists(f'/content/sample_data/{Model_Name}.tar.gz'):
  print("File not found.")
else:
  with tarfile.open(f'/content/sample_data/{Model_Name}.tar.gz','r:gz') as tar:
        tar.extractall('/content/RVC')

if os.path.exists(f'/content/RVC/weights'):
  !cp -R /content/RVC/weights /content/RVC/assets
  !rm -R /content/RVC/weights

#@title **Optional:** Download .pth File Of The Model

#@markdown  Use this code block to download the .pth file of model to use it anywhere.

# Step 1: Set the Model_Name variable
Model_Name = ""#@param {type:"string"}

# Step 2: Construct the file path
file_path = f'/content/RVC/assets/weights/{Model_Name}.pth'

# Step 3: Download the file
from google.colab import files

# Check if the file exists before attempting to download
import os
if os.path.exists(file_path):
    files.download(file_path)
else:
    print(f"File not found. Make sure that the model name is correct")

"""---"""

#@title **Step 1 :** Upload Target Audio
#@markdown The target audio file must be a very clean vocal audio.

import os
from IPython.display import Audio
from IPython.core.display import display

upload_method = 'Upload' #@param ['Upload']

#remove previous input audio
if os.path.isfile('/content/sample_data/input_audio.wav'):
    os.remove('/content/sample_data/input_audio.wav')

def displayAudio():
  display(Audio('/content/sample_data/input_audio.wav'))



if upload_method == 'Upload':
  from google.colab import files
  uploaded = files.upload()
  for fn in uploaded.keys():
    print('User uploaded file "{name}" with length {length} bytes.'.format(
        name=fn, length=len(uploaded[fn])))

##@markdown * لا تحتاج الي إعادة تسمية الملف

# Consider only the first file
PATH_TO_YOUR_AUDIO = str(list(uploaded.keys())[0])

# Load audio with specified sampling rate
import librosa
audio, sr = librosa.load(PATH_TO_YOUR_AUDIO, sr=None)

# Save audio with specified sampling rate
import soundfile as sf
sf.write('/content/sample_data/input_audio.wav', audio, sr, format='wav')

from IPython.display import clear_output
clear_output(wait=True)

displayAudio()

# Commented out IPython magic to ensure Python compatibility.
#@title **Step 2:** Run Inference
import os
import IPython.display as ipd
# %cd /content/RVC

#@markdown  Enter the name of the model you want to use.
model_name = 'ntkav'#@param {type:"string"}

model_filename = model_name + '.pth'
#index_filename = 'added_IVF156_Flat_nprobe_1_' + model_name + '_v2.index'

###########

# Setting .index File Name

#Create Folder temp .index file
# %cd /content

index_temp = 'Index_Temp'

if not os.path.exists(index_temp):
  os.mkdir(index_temp)
  print("Index_Temp Folder Created.")
else:
  print("Index_Temp Folder Found.")

#Copying .index file to Index_Temp folder

from os import listdir
import shutil

index_file_path = os.path.join('/content/RVC/logs/', model_name,'')

for file_name in listdir(index_file_path):
   if file_name.startswith('added') and file_name.endswith('.index'):
        shutil.copy(index_file_path + file_name, os.path.join( '/content/', index_temp, file_name))
        print("File exists")
        shutil.copyfile(index_file_path + file_name, os.path.join( '/content/', index_temp, file_name))
        print('Index File copied successfully.')

#Getting the name of .index file

# %cd /content/Index_Temp

import os

# Get the current working directory
indexfile_directory = os.getcwd()

# List all files in the current directory
files = os.listdir(indexfile_directory)

# Get the first filename from the list
first_filename = files[0]
print(first_filename)

# Save the filename as a variable
index_filename = first_filename

#Deleting Index_Temp folder

shutil.rmtree('/content/Index_Temp')

# %cd /content/RVC

#############

model_path = "/content/RVC/assets/weights/" + model_filename
index_path = "/content/RVC/logs/" + model_name + "/" + index_filename

#model_path = "/content/RVC/assets/weights/My-Voice.pth"#@param {type:"string"}
#index_path = "/content/RVC/logs/My-Voice/added_IVF439_Flat_nprobe_1_My-Voice_v2.index"#@param {type:"string"}

from colorama import Fore
print(Fore.GREEN + f"{index_path} was found") if os.path.exists(index_path) else print(Fore.RED + f"{index_path} was not found")

#@markdown ---
#@markdown **Set the "pitch" value if you are clonning...**

#@markdown **- Male to Male OR Female to Female : 0**

#@markdown **- Female to Male : -12**

#@markdown **- Male to Female : 12**

pitch = 6 # @param {type:"slider", min:-12, max:12, step:1}

#input_path = "/content/sample_data/input_audio.wav"#@param {type:"string"}
input_path = "/content/sample_data/input_audio.wav"

if not os.path.exists(input_path):
    raise ValueError(f"{input_path} was not found in your RVC folder.")
os.environ['index_root']  = os.path.dirname(index_path)
index_path = os.path.basename(index_path)

#@markdown ---

f0_method = "rmvpe" # @param ["rmvpe", "pm", "harvest"]

save_as = "/content/RVC/audios/kav1.wav"#@param {type:"string"}

model_name = os.path.basename(model_path)
os.environ['weight_root'] = os.path.dirname(model_path)
index_rate = 0.5 # @param {type:"slider", min:0, max:1, step:0.01}
volume_normalization = 0 #param {type:"slider", min:0, max:1, step:0.01}
consonant_protection = 0.5 #param {type:"slider", min:0, max:1, step:0.01}

!rm -f $save_as

!python tools/cmd/infer_cli.py --f0up_key $pitch --input_path $input_path --index_path $index_path --f0method $f0_method --opt_path $save_as --model_name $model_name --index_rate $index_rate --device "cuda:0" --is_half True --filter_radius 3 --resample_sr 0 --rms_mix_rate $volume_normalization --protect $consonant_protection

#show_errors = True #@param {type:"boolean"}
show_errors = True

if not show_errors:
    ipd.clear_output()
ipd.Audio(save_as)

#@title **Step 3 :** Download Output Audio
#@markdown * Use this cell to download the final converted audio file.
#@markdown * If the final audio file is longer than 4 minutes, The preview may not show up in the previous step. But it is already converted and you can download it using this cell.

from google.colab import files

# Specify the file path
file_path = '/content/RVC/audios/output_audio.wav'

# Download the file
files.download(file_path)