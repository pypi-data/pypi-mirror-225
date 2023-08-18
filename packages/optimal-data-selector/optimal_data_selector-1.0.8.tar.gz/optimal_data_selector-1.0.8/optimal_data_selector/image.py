def web_image_downloader(file_path,url,img_tag='img',tag_sc='src',n_image=20,extention=".jpg",state=0,keep='all',exception=None,img_download_status=False):
    """
    Scrapes images  from  given webpage and downloads specified images to a directory , it allows you to choose
    the number of images and as well as you can choose any perticular image or also can ignore any image or set
    of images.

    Args:
        * file_path (str)   : Directory path where images will be saved, make sure that you are using 
                              forward slash "/" in the file path, and dot forget to apply another
                              forword slash to the end of the path : like ['C:/downloaded_images/'].
        
        * url (str)     : URL of the webpage to scrape images from.
        
        * img_tag (str, optional)    : HTML tag to identify the images, detail info is 
                                       available to the 'Tutorials section'. Default is 'img'.
        
        * tag_sc (str, optional)   : Attribute of the image tag containing the image URL,detail info is 
                                    available to the 'Tutorials section . Default is 'src'.
        
        * n_image (int, optional)  : Maximum number of images to be scraped. Default is 20.
        
        * extention (str, optional)  : File extension to be added to saved images, make sure
                                       that you are using '.jpg' or '.png' instead writng 
                                       only 'jpg' or 'png',[only 'jpg' or 'png' can throw
                                       error] . Default is '.jpg'.
        
        * state (int, optional)  : Starting index for naming downloaded images, detail info is 
                                   available to the 'Tutorials' section. Default is 0.
        
        * keep (str or list, optional) : Specify which images to keep using indices or 'all', make sure
                                         the value is a list object 
                                          ** like : keep=[0,2,5,6]. Default is 'all'.
        
        * exception (list, optional)  : List of indices to exclude images from downloading make sure
                                         the value is a list object 
                                          ** like : exception=[0,2,5,6]. Default is None.
        
        * img_download_status (bool, optional)  : If True, prints download status for each image. Default is False.
        

    Returns:
        It returns two elements - the number of images downloaded and a success message.

    Examples:
        # Download all images from the given URL
        image_sc(file_path='downloaded_images/', url='https://example.com/page-with-images')

        # Download specific images using their indices
        image_sc(file_path='downloaded_images/', url='https://example.com/page-with-images',
                 keep=[0, 2, 5, 8])

        # Download images excluding specific indices
        image_sc(file_path='downloaded_images/', url='https://example.com/page-with-images',
                 exception=[3, 6, 9])

        # Download images and print download status
        image_sc(file_path='downloaded_images/', url='https://example.com/page-with-images',
                 img_download_status=True)
                 
    Tutorials :
            Quarry-1: How to get proper image tag ?
            Ans:      Go the web page --> right click on any image --> click to the "Inspect" option --> find "<img" tag -->
                      from there find "src" or "srcset" --> copy the common part from the given 'https'
                 
                 #Example
                        Let suppose we have two https like : " src"=https://img.freepik.com/free-photo/portrait-handsome-smiling-stylish-hipster-
                                                                    lambersexual-model-sexy-man-dressed-pink-tshirt
                                                                    -trousers-fashion-male-isolated-blue-wall-studio_158538-26677.jpg
                                                                    
                                                             " src"=https://img.freepik.com/premium-photo/young-brazilian-man-isolated-
                                                                     blue-background-with-glasses-happy-expression_1368-356771.jpg   
                                                                     
                        *** So here --> 'https://img.freepik.com'  is the common part among these two 'https'
                        
           Quarry-2: How to write image tag ?
           Ans:      We have copied "https://img.freepik.com" from "src" because it is the common part for all the images
           
                     ***write it like this ---> img_tag = 'img[src^="https://img.freepik.com"]'
           
           Quarry-3 What should be the ideal value of tag_sc perameter?
           Ans:     It can be "src" and sometimes it canbe "srcset" to, now it totally depends on the
                     user, you can put other values for experiment
                     
           Quarry-4 What does the state perameter value refer ?
           Ans:     It refers that an ideal value that will prevents the image loss
                    and the function returns the ideal state value, just write that
                    as the value of state paremeter, if you are using same directory 
                    to save the images multiple times 
                     
        
    """
    
    #!pip install lxml
    from bs4 import BeautifulSoup
    import requests
    import urllib.request
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}
    session = requests.Session()
    
    e_ind=[] 
    k_ind=[] 
    
    try:
        #res=session.get(url,headers=headers)
        #res.raise_for_status()
        source = requests.get(url,headers=headers).text
        soup= BeautifulSoup(source,'html.parser')
        Images=[]
        img_links= soup.select(img_tag)
    
        for i in range(len(img_links)):
            Images.append(img_links[i][tag_sc])
            if len(Images) == n_image:
                break
        le=len(Images)   
        end=state+le
        
        #print("Next state Value would be = "+str(state+len(Images)))
        print('Trying to load all the images........')
        
        if keep == 'all' and exception == None :
            print("Next state Value would be = "+str(state+len(Images)))
            for r,l in enumerate(Images,start=state):
            #for r in range(len(Images)):
                name= file_path+str(r)+extention
                urllib.request.urlretrieve(l, name)
                if img_download_status == True:
                    print('img:',r,' downloaded')
                
            if len(Images) != n_image:    
                print(len(Images),'Images Found')
            elif len(Images) == n_image:
                print('All images has been Downloaded Successfully')
            return  len(Images),'Images saved to the directory'    
                
               
        elif exception != None :
            for z in exception:
                e_ind.append(Images[z])
            for d in e_ind:
                Images.remove(d)
            print("Next state Value would be = "+str(state+len(Images)))    
            for r,l in enumerate(Images,start=state):
            #for r in range(len(Images)):
                name= file_path+str(r)+extention
                urllib.request.urlretrieve(l, name) 
                if img_download_status == True:
                    print('img:',r,' downloaded')
                
            if len(Images) != n_image:    
                print(len(Images),'Images Found')
            elif len(Images) == n_image:
                print('All images has been Downloaded Successfully') 
            return len(Images),'Images saved to the directory'     
                
               
        elif keep != 'all':
            for o in keep:
                k_ind.append(Images[o])
            print("Next state Value would be = "+str(state+len(k_ind)))    
            for r,l in enumerate(k_ind,start=state):
            #for r in range(len(Images)):
                name= file_path+str(r)+extention
                urllib.request.urlretrieve(l, name) 
                if img_download_status == True:
                    print('img:',r,' downloaded')
                
            if len(k_ind) != n_image:    
                print(len(k_ind),'Images Found')
            elif len(k_ind) == n_image:
                print('All images has been Downloaded Successfully')
            return len(k_ind),'Images saved to the directory'    
                
            
    except Exception as ex:
        print(ex)