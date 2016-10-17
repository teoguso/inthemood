from heuro_api import Heuro
from credentials import email, password

myhero = Heuro(email, password)
audio_pipe = 1747

#ingest = myhero.ingest_file('../data/audio/tom_scott_trim.mp3', audio_pipe)
pipelinekey = 'K_ba0b77e0_de9c_41ee_9c30_1927ba646790'
#pipelinekey = ingest['pipelinekey']
#print pipelinekey

print myhero.get_results(audio_pipe, pipelinekey).json()

