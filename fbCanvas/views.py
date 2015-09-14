from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import base64

@csrf_exempt
def index(request):
	context={}
	#1623981184542944
	#ebeabb8aabca0cc1469df0a681f989f0
	import pdb; pdb.set_trace();
	return render(request, 'fbCanvas/index.html', context)

def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'='* missing_padding
    return base64.decodestring(data)