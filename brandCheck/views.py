from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render_to_response
import os, string, re, requests, csv

# Create your views here.
def index(request):
	file = open(os.path.abspath('brands_list_from_marc.txt'), 'r')
	context = {}
	brandInfo = []
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="brand_results.csv"'
	writer = csv.writer(response)
	writer.writerow([ 'name',
					'url',
					'chute',
					'tint',
					'olapic',
					'postano',
					'curalate',
					'foursixty',
					'twitter_widget',
					'pixlee',
					'sociable',
					'instagram',
					'twitter',
					'linkedin',
					'tumblr',
					'facebook',
					'googleplus2',
					'pinterest',
					'googleplus',
					'youtube',
					'flickr',
					'email'])
	for line in file:
		alias = None
		alias_response = 'N/A'
		if '(' in line:
			line = line.split('(')
			alias = line[1]
			brandInfo.append(prepAndGet(alias, writer))
			line = line[0]
		#erase line spaces
		brandInfo.append(prepAndGet(line, writer))
		#print 'line response:', line, line_response
		#print 'alias response:', alias, alias_response
		context['brandInfo'] = brandInfo
	#import pdb; pdb.set_trace();
	#return render(request, 'brandCheck/index.html', context)
	return response


def prepAndGet(brand, writer):
	brand = brand.split(')')[0]
	brand = brand.strip()
	brand = brand.lower()
	brand = brand.replace(' ', '')
	brand = brand.translate(string.maketrans("",""), string.punctuation)
	brand_info = {}
	brand_info['name'] = brand
	brand_result_list = []
	brand_result_list.append(brand)
	competitor_tells = {'olapic':'olapic',
						'sociable': 'sociable',
						'postano': 'postano',
						'tint': 'tintup',
						'pixlee': 'pixlee',
						'curalate': 'curalate',
						'chute': 'chute',
						'foursixty': 'foursixty', 
						'twitter_widget': 'twitter.com/widgets', #data-timeline-type could be more accurate
						'readypulse':'readypulse',
						'percolate': 'percolate',
						#'tintup2': 'cloudfront.net/tint/'
						}

	social_media = {
					'facebook':'href=\".*facebook.com/([^\"]*)\"',
					'tumblr':'href=\"([^\".]*).*tumblr.com',
					'twitter': 'href=\".*twitter.com/([^\"]*)\"',
					'instagram':'href=\".*instagram.com/([^\"]*)\"',
					'linkedin':'href=\".*linkedin.com/company/([^\"]*)\"',
					'youtube':'href=\".*youtube.com/([^\"]*)\"',
					'googleplus':'href=\".*plus.google.com/([^\"]*)\"',
					'googleplus2':'href=\".*plus.google.com/posts/([^\"]*)\"', 
					'flickr':'href=\".*flickr.com/photos/([^\"]*)\"',
					'pinterest': 'href=\".*pinterest.com/([^\"]*)\"',
					'email': 'href=\"mailto:([^\"]*)\"'
					}
	try:
		brand_response = requests.get('http://www.'+brand+'.com', timeout = 5)
		if brand_response.status_code != 200:
			raise requests.exceptions.RequestException
		brand_result_list.append('http://www.'+brand+'.com')
		brand_info['website_works'] = True
		for competitor in competitor_tells:
			if re.search(competitor_tells[competitor], brand_response.text):
				brand_result_list.append(True)
				brand_info[competitor] = True
			else:
				brand_result_list.append(False)
				brand_info[competitor] = False
		for platform in social_media:
			social_id = "N/A"
			if re.search(social_media[platform], brand_response.text):
				social_id = re.search(social_media[platform], brand_response.text).group(1).strip('/').split('/')[-1].split('?')[0]
				social_id = social_id.encode('ascii','ignore') 
			brand_info[platform] = social_id 
			brand_result_list.append(social_id)
	except requests.exceptions.RequestException as e:
		brand_result_list.append('')
		brand_info['website_works'] = False
		for competitor in competitor_tells:
			brand_info[competitor] = False
			brand_result_list.append(False)
		for platform in social_media:
			brand_info[competitor] = False
			brand_result_list.append('N/A')
	writer.writerow(brand_result_list)
	print brand_info
	return brand_info


