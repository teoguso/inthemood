from heuro_api import Heuro
from credentials import email, password, pipeline_id

myhero = Heuro(email, password)

pipe = myhero.make_pipeline('test_pipe123')
print pipe