from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2 as ur

register_openers()

UPLOAD_URL = "http://localhost:9000/v1/pipelines/1/ingestfile"

def upload_batch(fname):
	with open(fname, 'r') as f:
	    	datagen, hs = multipart_encode({"file": f})
		hs['Key']="PUT YOUR KEY HERE"
		req = ur.Request(UPLOAD_URL,  datagen,  hs)
		response = ur.urlopen(req).read()
		print(response)


def main():
	upload_batch("/home/ibrahim/pom.xml")

if __name__ == "__main__":
	main()
