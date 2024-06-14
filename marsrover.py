import requests
import json
import webbrowser
import random

api_key = "api key"
api_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/'

def get_photos(rover, sol, camera):
    sol_pic = False
    retry_count = 0
    while not sol_pic:
        r = requests.get(api_url + rover + '/photos?sol=' + str(sol) + '&camera=' + camera + '&api_key=' + api_key)
        if r.status_code != 200:
            print(f"Error {r.status_code} while fetching photos for rover {rover} on Sol {sol} with camera {camera}")
            return []
        data = r.json()
        
        if data['photos'] or retry_count > 2:
            sol_pic = True
        else:
            sol -= 1
            retry_count += 1

    return data['photos']

def rover():
    
    params = {"sol":"5111", "api_key": api_key}
    f = r"https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos?"
    data = requests.get(f, params = params)
    a = json.loads(data.text)
    
    for i in a["photos"]:
        print(i, "\n\n\n")
    
        b = a["photos"][0]["img_src"]
        print(a["photos"][0]["img_src"])
    
    webbrowser.open(b)

rovers = ['curiosity', 'opportunity', 'perseverance']
cameras = ['chemcam', 'fhaz', 'navcam', 'rhaz', 'mast', 'mahli', 'mardi', 'pancam', 'minites']

def mars_images(rover, sol, camera):
    images = []
    sol_pic = False
    retry_count = 0
    while not sol_pic:
        #set random rover
        ran_rover = random.choice(rovers)

        #filter rover argument
        if rover == '' or rover.lower() not in rovers or str(rover).isdigit() == True:
            rover = ran_rover
        else:
            rover = rover
        
        #max sols
        e = requests.get(api_url + rover + '/?api_key=' + api_key)
        if e.status_code != 200:
            print(f"Error {e.status_code} while fetching photos for rover {rover} on Sol {sol} with camera {camera}")
            return ['Unavailable']
        temp = e.json()
        sols = temp['rover']['max_sol']

        #filter sol argument
        if str(sol).isdigit() == False:
            sol = sols
        elif int(sol) > sols or sol == -1:
            sol = sols
        else:
            sol = sol

        #filter camera argument
        if camera == '' or camera.lower() not in cameras or str(camera).isdigit() == True:

            #only takes the first image
            r = requests.get(api_url + rover + '/photos?sol=' + str(sol) + '&api_key=' + api_key)
            r_json = r.json()
            pic_nocam = r_json['photos'][0]['img_src']
            pic = []
            pic.append(f"{pic_nocam}")

            return pic, sols
        
        else:

            r = requests.get(api_url + rover + '/photos?sol=' + str(sol) + '&camera=' + camera + '&api_key=' + api_key)
            if r.status_code != 200:
                print(f"Error {e.status_code} while fetching photos for rover {rover} on Sol {sol} with camera {camera}")
                return ['Unavailable']
            data = r.json()

            if len(data['photos']) == 0:
                images.append('No Cam available')
                
                return images, sols
            
            else:
                print(data)
                all_cam = data['photos'][0]['rover']['cameras']
                c = []
                for e in range(len(all_cam)):
                    c.append(all_cam[e]['name'])
                if camera.upper() not in c:
                    images.append('Cam not available')

                    return c, sols
                
                else:
                    #print images
                    for i in data['photos']:
                        print(i, "\n\n\n")

                    #append to a list
                    y = len(data['photos'])
                    img_withcam = []
                    for k in range(y)[:5]:
                        b = data['photos'][k]['img_src']
                        img_withcam.append(f"{b}")

                    print(sols)
                    return img_withcam, sols
            

#message = mars_images('curiosty', 1000, '')
#for k in message:
    #print(k)
#print(mars_images('curiosity', 200, 'navcam'))