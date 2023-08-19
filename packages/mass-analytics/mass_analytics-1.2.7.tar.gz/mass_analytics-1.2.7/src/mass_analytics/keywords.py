import requests
import json


gist_id = "c36a2a2a5f11f72ae40a7425f36bd3f7"
file_name = "Keywords.json" 

def see_all():
    """
    Fetches JSON content from a specific file within a GitHub Gist.

    Args:
        gist_id (str): The unique identifier of the GitHub Gist.
        file_name (str): The name of the JSON file within the Gist.

    Returns:
        dict: A dictionary containing the parsed JSON content from the specified file.

    Raises:
        Exception: If the Gist or file retrieval fails, or if there is an error parsing JSON content.

    Note:
        This function utilizes the GitHub Gist API to fetch the content of a specified file within a Gist.
        The content is assumed to be in JSON format, and this function attempts to parse it as such.
    """

    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)
 
    if response.status_code == 200:
        gist_data = response.json()
        if file_name in gist_data["files"]:
            content = gist_data["files"][file_name]["content"]
            try:
                json_content = json.loads(content)
                return json_content
            except json.JSONDecodeError:
                raise Exception("Error parsing JSON content")
        else:
            raise Exception("File not found in Gist")
    else:
        raise Exception("Failed to fetch Gist")
    
def add_value(category, key, value, access_token):
    """
    Add a value to a JSON file in a GitHub Gist.

    Args:
        category (str): The category under which the key-value pair should be added.
        key (str): The key within the specified category.
        value: The value to be added to the JSON file.

    This function retrieves the current content of a JSON file within a GitHub Gist,
    adds a new value to the specified category and key, and updates the Gist with
    the modified content.

    Note:
        - The function will prompt you to input your GitHub Personal Access Token.
        - Make sure the specified category/key exist.
        - The function handles possible errors related to JSON decoding, category, and key.

    Raises:
        Exception: If the Gist or file is not found, access token is incorrect,
                   JSON content cannot be parsed, or the category/key is invalid.
    """

    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Fetch the current Gist data
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)

    if response.status_code == 200:
        gist_data = response.json()
        
        if file_name in gist_data["files"]:
            file_data = gist_data["files"][file_name]
            content = file_data["content"]
            try:
                json_content = json.loads(content)
            except json.JSONDecodeError:
                raise Exception("Error parsing JSON content")
            try:
                json_content[category][key].append(value)
            except:
                if category not in json_content.keys():
                    raise Exception("Please select the appropriate category; you must choose from these options: "+str(list(json_content.keys())))
                keys = json_content[category].keys()
                if key not in keys:
                    raise Exception("Please select the appropriate key; you must choose from these options: "+str(list(keys)))
            
            file_data["content"] = json.dumps(json_content, indent=4)

            # Update the Gist content
            data = {
                "files": {
                    file_name: file_data
                }
            }
            update_response = requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data)

            if update_response.status_code == 200:
                print("Gist content updated successfully.")
            else:
                raise Exception("Failed to update Gist content")
        else:
            raise Exception("File not found in Gist")
    else:
        raise Exception("Failed to fetch Gist maybe wrong access token")

def reset_all(access_token):
    """
    Reset specified data within a GitHub Gist JSON file using the provided access token.

    This function resets predefined sections of data within a JSON file hosted in a GitHub Gist.
    The predefined data includes media channels, campaign categories, campaign objectives, and media metrics.

    The function prompts the user for an access token, retrieves the Gist data, resets the specified content,
    and updates the Gist with the new content.

    Raises:
        Exception: If there are errors during JSON parsing, updating the Gist, or other API-related issues.

    Usage:
        Call this function to reset specific sections of JSON data within a GitHub Gist.

    Example:
        reset_all()
    """
    
    reset_data = {
        "Media Channels": {
            "Facebook": [
                "fb",
                "facebook",
                "fb ads",
                "facebook ads",
                "fb marketing",
                "facebook marketing"
            ],
            "YouTube": [
                "youtube",
                "yt",
                "youtube videos",
                "yt ads",
                "youtube advertising",
                "video marketing"
            ],
            "Google Ads": [
                "googleads",
                "google ads",
                "adwords",
                "google advertising",
                "search ads",
                "google ad campaign"
            ],
            "Instagram": [
                "instagram",
                "ig",
                "insta",
                "instagram ads",
                "ig marketing",
                "insta ads",
                "instagram advertising"
            ],
            "Twitter": [
                "twitter",
                "tweets",
                "twitter ads",
                "twitter marketing",
                "twitter platform",
                "twitter campaign"
            ],
            "LinkedIn": [
                "linkedin",
                "li",
                "linkedin ads",
                "li marketing",
                "linkedin campaign",
                "linkedin advertising"
            ],
            "Pinterest": [
                "pinterest",
                "pins",
                "pinterest ads",
                "pinterest marketing",
                "pinterest platform",
                "pinterest campaign"
            ],
            "Snapchat": [
                "snapchat",
                "snap",
                "snap chat",
                "sc",
                "snap lens",
                "snap ad"
            ],
            "TikTok": [
                "tiktok",
                "tik tok",
                "tt",
                "tiktok video",
                "tiktok ad",
                "tiktok campaign",
                "tiktok challenge",
                "tiktok sound",
                "tiktok influencer",
                "tiktok trend"
            ]
        },
        "Campaign Categories": {
            "Display": [
                "display",
                "banner",
                "ad banner",
                "banner ad",
                "display ad",
                "web banner"
            ],
            "Native": [
                "native",
                "in-feed",
                "in-feed ad",
                "native ad",
                "content ad",
                "sponsored content",
                "native advertising",
                "in-feed promotion",
                "contextual ad",
                "seamless ad"
            ],
            "CTV": [
                "ctv",
                "connected tv",
                "smart tv",
                "internet tv",
                "OTT",
                "over-the-top",
                "streaming tv",
                "tv streaming",
                "connected television",
                "smart television"
            ],
            "Social": [
                "social",
                "social media",
                "social platform",
                "social network",
                "social advertising",
                "social marketing",
                "social campaign",
                "social strategy",
                "social engagement",
                "social presence"
            ],
            "Search": [
                "search",
                "search ads",
                "search engine marketing",
                "paid search",
                "search campaign",
                "search results",
                "keyword advertising",
                "SEM",
                "PPC",
                "pay-per-click"
            ],
            "Video": [
                "video",
                "video ads",
                "video marketing",
                "video campaign",
                "video content",
                "video production",
                "video promotion",
                "video platform",
                "video sharing",
                "video views"
            ],
            "Email": [
                "email",
                "email marketing",
                "email campaign",
                "email promotion",
                "email newsletter",
                "email blast",
                "email list",
                "email automation",
                "email open rate",
                "click-through rate"
            ],
            "Print": [
                "print",
                "print ads",
                "print media",
                "print advertising",
                "magazine ads",
                "newspaper ads",
                "brochure",
                "catalog",
                "direct mail",
                "printed materials"
            ],
            "Outdoor": [
                "outdoor",
                "billboard",
                "out-of-home",
                "OOH",
                "street signage",
                "transit ads",
                "bus stop ads",
                "outdoor advertising",
                "outdoor campaign",
                "outdoor media"
            ]
        },
        "Campaign Objectives": {
            "Awareness": [
                "awareness",
                "brand awareness",
                "raise awareness",
                "increase visibility",
                "visibility campaign",
                "mindshare",
                "attention",
                "perception"
            ],
            "Reach": [
                "reach",
                "audience reach",
                "wider audience",
                "extend reach",
                "reach campaign",
                "expanding audience",
                "maximize exposure",
                "broaden impact"
            ],
            "Traffic": [
                "traffic",
                "website traffic",
                "increase traffic",
                "drive visits",
                "web visits",
                "boost web traffic",
                "site visits",
                "online traffic",
                "visitor volume"
            ],
            "Conversion": [
                "conversion",
                "increase conversions",
                "drive conversions",
                "conversion rate",
                "lead conversion",
                "sales conversion",
                "conversion optimization",
                "conversion funnel"
            ],
            "Sales": [
                "sales",
                "increase sales",
                "boost revenue",
                "sales growth",
                "sales campaign",
                "sales-driven",
                "sales conversion",
                "sales performance",
                "sales target"
            ],
            "Lead Generation": [
                "lead generation",
                "generate leads",
                "lead acquisition",
                "lead campaign",
                "lead nurturing",
                "lead qualification",
                "lead capture",
                "lead funnel",
                "lead magnet"
            ],
            "Brand Engagement": [
                "brand engagement",
                "engage with brand",
                "brand interaction",
                "brand participation",
                "brand connection",
                "brand involvement",
                "brand experience",
                "brand affinity",
                "brand loyalty"
            ],
            "App Installs": [
                "app installs",
                "mobile app installs",
                "install app",
                "download app",
                "app download",
                "app installation",
                "app acquisition",
                "app store installs",
                "get the app",
                "install now"
            ],
            "Customer Acquisition": [
                "customer acquisition",
                "acquire customers",
                "acquiring customers",
                "gain new customers",
                "customer growth",
                "customer recruitment",
                "customer onboarding",
                "customer conversion",
                "customer procurement"
            ]
        },
        "Media Metrics": {
            "Impression": [
                "impression",
                "impressions",
                "ad impression",
                "viewed impression",
                "impression count",
                "impression tracking",
                "ad exposure",
                "viewable impression",
                "ad view"
            ],
            "Clicks": [
                "click",
                "clicks",
                "ad click",
                "link click",
                "click-through",
                "click-throughs",
                "click rate",
                "interaction click",
                "engagement click",
                "click tracking"
            ],
            "CTR (Click-Through Rate)": [
                "ctr",
                "click-through rate",
                "click rate",
                "link click rate",
                "CTR metric",
                "CTR analysis",
                "CTR measurement",
                "click-through ratio",
                "interaction rate",
                "engagement rate"
            ],
            "CPM (Cost Per Mille)": [
                "cpm",
                "cost per mille",
                "cost per thousand",
                "mille cost",
                "CPM rate",
                "CPM calculation",
                "advertising cost per mille",
                "CPM pricing",
                "mille rate",
                "CPM analysis"
            ],
            "CPC (Cost Per Click)": [
                "cpc",
                "cost per click",
                "click cost",
                "click pricing",
                "CPC rate",
                "CPC calculation",
                "advertising cost per click",
                "CPC model",
                "click expense",
                "CPC analysis"
            ],
            "CPA (Cost Per Acquisition)": [
                "cpa",
                "cost per acquisition",
                "acquisition cost",
                "conversion cost",
                "CPA rate",
                "CPA calculation",
                "advertising cost per acquisition",
                "CPA model",
                "acquisition expense",
                "CPA analysis"
            ],
            "ROAS (Return On Ad Spend)": [
                "roas",
                "return on ad spend",
                "ad spend return",
                "ROAS ratio",
                "ROAS calculation",
                "return on investment",
                "advertising ROI",
                "advertising return",
                "ROAS analysis",
                "ROAS measurement"
            ],
            "Conversion Rate": [
                "conversion rate",
                "rate of conversion",
                "conversion ratio",
                "conversion percentage",
                "conversion efficiency",
                "conversion analysis",
                "conversion tracking",
                "conversion benchmark",
                "conversion success",
                "rate of success"
            ],
            "Viewability": [
                "viewability",
                "ad viewability",
                "viewable impressions",
                "viewable ad",
                "ad visibility",
                "visible impression",
                "ad display",
                "viewability measurement",
                "viewability analysis",
                "viewability standards"
            ],
            "Engagement": [
                "engagement",
                "ad engagement",
                "user engagement",
                "audience engagement",
                "engagement rate",
                "engagement level",
                "interaction",
                "user interaction",
                "audience interaction",
                "engagement measurement"
            ],
            "Video Views": [
                "video views",
                "views",
                "video impressions",
                "video playbacks",
                "video visibility",
                "watched views",
                "video engagement",
                "video viewer count",
                "play count",
                "video performance"
            ]
        }
    }
    
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Fetch the current Gist data
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)

    if response.status_code == 200:
        gist_data = response.json()
        
        if file_name in gist_data["files"]:
            file_data = gist_data["files"][file_name]
            content = file_data["content"]
            try:
                json_content = json.loads(content)
            except json.JSONDecodeError:
                raise Exception("Error parsing JSON content")
            
            json_content = reset_data
            
            file_data["content"] = json.dumps(json_content, indent=4)

            # Update the Gist content
            data = {
                "files": {
                    file_name: file_data
                }
            }
            update_response = requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data)

            if update_response.status_code == 200:
                print("Gist content updated successfully.")
            else:
                raise Exception("Failed to update Gist content")
        else:
            raise Exception("File not found in Gist")
    else:
        raise Exception("Failed to fetch Gist maybe wrong access token")
    
def add_key(category, key, access_token):
    """
    Add a new key to a category within a JSON file in a GitHub Gist using the provided access token.

    This function adds a new key to a specified category in a JSON file hosted in a GitHub Gist.
    The new key is initialized with an empty list. If the category does not exist, an error is raised.

    Args:
        category (str): The name of the category to which the new key will be added.
        key (str): The name of the new key to be added.
        access_token (str): The GitHub access token for authorization.

    Raises:
        Exception: If there are errors during JSON parsing, updating the Gist, or other API-related issues.
                  If the specified category does not exist within the JSON data.

    Usage:
        Call this function to add a new key with an empty list to a category in a JSON file within a GitHub Gist.

    Example:
        add_key("Media Channels", "NewKey", "your-access-token")
    """

    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Fetch the current Gist data
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)

    if response.status_code == 200:
        gist_data = response.json()
        
        if file_name in gist_data["files"]:
            file_data = gist_data["files"][file_name]
            content = file_data["content"]
            try:
                json_content = json.loads(content)
            except json.JSONDecodeError:
                raise Exception("Error parsing JSON content")
            try:
                json_content[category][key] = []
            except:
                if category not in json_content.keys():
                    raise Exception("Please select the appropriate category; you must choose from these options: "+str(list(json_content.keys())))
            
            file_data["content"] = json.dumps(json_content, indent=4)

            # Update the Gist content
            data = {
                "files": {
                    file_name: file_data
                }
            }
            update_response = requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data)

            if update_response.status_code == 200:
                print("Gist content updated successfully.")
            else:
                raise Exception("Failed to update Gist content")
        else:
            raise Exception("File not found in Gist")
    else:
        raise Exception("Failed to fetch Gist maybe wrong access token")
    
def add_category(category, access_token):
    """
    Add a new category to a JSON file within a GitHub Gist using the provided access token.

    This function adds a new category and initializes it with an empty dictionary in a JSON file hosted in a GitHub Gist.
    The category name and its corresponding empty dictionary will be added to the JSON data.

    Args:
        category (str): The name of the category to be added.
        access_token (str): The GitHub access token for authorization.

    Raises:
        Exception: If there are errors during JSON parsing, updating the Gist, or other API-related issues.

    Usage:
        Call this function to add a new category with an empty dictionary to a JSON file in a GitHub Gist.

    Example:
        add_category("NewCategory", "your-access-token")
    """

    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Fetch the current Gist data
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)

    if response.status_code == 200:
        gist_data = response.json()
        
        if file_name in gist_data["files"]:
            file_data = gist_data["files"][file_name]
            content = file_data["content"]
            try:
                json_content = json.loads(content)
            except json.JSONDecodeError:
                raise Exception("Error parsing JSON content")
            
            json_content[category] = {}
            
            file_data["content"] = json.dumps(json_content, indent=4)

            # Update the Gist content
            data = {
                "files": {
                    file_name: file_data
                }
            }
            update_response = requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data)

            if update_response.status_code == 200:
                print("Gist content updated successfully.")
            else:
                raise Exception("Failed to update Gist content")
        else:
            raise Exception("File not found in Gist")
    else:
        raise Exception("Failed to fetch Gist maybe wrong access token")

def remove_value(category, key, value, access_token):
    """
    Remove a value from a key within a category in a JSON file in a GitHub Gist using the provided access token.

    This function removes a specified value from a key within a category in a JSON file hosted in a GitHub Gist.
    If the specified category, key, or value does not exist, an error is raised.

    Args:
        category (str): The name of the category containing the key and value to be removed.
        key (str): The name of the key from which the value will be removed.
        value (str): The value to be removed from the specified key within the category.
        access_token (str): The GitHub access token for authorization.

    Raises:
        Exception: If there are errors during JSON parsing, updating the Gist, or other API-related issues.
                  If the specified category, key, or value does not exist within the JSON data.

    Usage:
        Call this function to remove a value from a key within a category in a JSON file within a GitHub Gist.

    Example:
        remove_value("Media Channels", "Facebook", "facebook", "your-access-token")
    """

    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Fetch the current Gist data
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)

    if response.status_code == 200:
        gist_data = response.json()
        
        if file_name in gist_data["files"]:
            file_data = gist_data["files"][file_name]
            content = file_data["content"]
            try:
                json_content = json.loads(content)
            except json.JSONDecodeError:
                raise Exception("Error parsing JSON content")
            try:
                json_content[category][key].remove(value)
            except:
                if category not in json_content.keys():
                    raise Exception("Please select the appropriate category; you must choose from these options: "+str(list(json_content.keys())))
                keys = json_content[category].keys()
                if key not in keys:
                    raise Exception("Please select the appropriate key; you must choose from these options: "+str(list(keys)))
                raise Exception("Value doesn\'t exist : "+ value)
            
            file_data["content"] = json.dumps(json_content, indent=4)

            # Update the Gist content
            data = {
                "files": {
                    file_name: file_data
                }
            }
            update_response = requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data)

            if update_response.status_code == 200:
                print("Gist content updated successfully.")
            else:
                raise Exception("Failed to update Gist content")
        else:
            raise Exception("File not found in Gist")
    else:
        raise Exception("Failed to fetch Gist maybe wrong access token")
    
def remove_key(category, key, access_token):
    """
    Remove a key from a category in a JSON file in a GitHub Gist using the provided access token.

    This function removes a specified key from a category in a JSON file hosted in a GitHub Gist.
    If the specified category or key does not exist, an error is raised.

    Args:
        category (str): The name of the category from which the key will be removed.
        key (str): The name of the key to be removed from the specified category.
        access_token (str): The GitHub access token for authorization.
    
    Raises:
        Exception: If there are errors during JSON parsing, updating the Gist, or other API-related issues.
                  If the specified category or key does not exist within the JSON data.

    Usage:
        Call this function to remove a key from a category in a JSON file within a GitHub Gist.

    Example:
        remove_key("Media Channels", "Facebook", "your-access-token")
    """

    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Fetch the current Gist data
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)

    if response.status_code == 200:
        gist_data = response.json()
        
        if file_name in gist_data["files"]:
            file_data = gist_data["files"][file_name]
            content = file_data["content"]
            try:
                json_content = json.loads(content)
            except json.JSONDecodeError:
                raise Exception("Error parsing JSON content")
            try:
                json_content[category].pop(key)
            except:
                if category not in json_content.keys():
                    raise Exception("Please select the appropriate category; you must choose from these options: "+str(list(json_content.keys())))
                raise Exception("Wrong key : "+key)
            
            file_data["content"] = json.dumps(json_content, indent=4)

            # Update the Gist content
            data = {
                "files": {
                    file_name: file_data
                }
            }
            update_response = requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data)

            if update_response.status_code == 200:
                print("Gist content updated successfully.")
            else:
                raise Exception("Failed to update Gist content")
        else:
            raise Exception("File not found in Gist")
    else:
        raise Exception("Failed to fetch Gist maybe wrong access token")
    
def remove_category(category, access_token):
    """
    Remove a category from a JSON file in a GitHub Gist using the provided access token.

    This function removes a specified category along with all its keys and values from a JSON file hosted in a GitHub Gist.
    If the specified category does not exist, an error is raised.

    Args:
        category (str): The name of the category to be removed.
        access_token (str): The GitHub access token for authorization.

    Raises:
        Exception: If there are errors during JSON parsing, updating the Gist, or other API-related issues.
                  If the specified category does not exist within the JSON data.

    Usage:
        Call this function to remove a category and its contents from a JSON file within a GitHub Gist.

    Example:
        remove_category("Media Channels", "your-access-token")
    """

    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Fetch the current Gist data
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)

    if response.status_code == 200:
        gist_data = response.json()
        
        if file_name in gist_data["files"]:
            file_data = gist_data["files"][file_name]
            content = file_data["content"]
            try:
                json_content = json.loads(content)
            except json.JSONDecodeError:
                raise Exception("Error parsing JSON content")
            
            json_content.pop(category)
            
            file_data["content"] = json.dumps(json_content, indent=4)

            # Update the Gist content
            data = {
                "files": {
                    file_name: file_data
                }
            }
            update_response = requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data)

            if update_response.status_code == 200:
                print("Gist content updated successfully.")
            else:
                raise Exception("Failed to update Gist content")
        else:
            raise Exception("File not found in Gist")
    else:
        raise Exception("Failed to fetch Gist maybe wrong access token")
    
def update_data(dictionary, access_token):
    """
     Update a specific file's content within a GitHub Gist using the provided dictionary.
    
    Args:
        dictionary (dict): The dictionary containing the data to update the file with.
        access_token (str): The GitHub access token for authentication.
    
    Raises:
        Exception: If there are errors during the process such as fetching Gist data, JSON decoding,
                   updating the Gist content, or if the provided file is not found in the Gist.
    """

    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Fetch the current Gist data
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)

    if response.status_code == 200:
        gist_data = response.json()
        
        if file_name in gist_data["files"]:
            file_data = gist_data["files"][file_name]
            content = file_data["content"]
            try:
                json_content = json.loads(content)
            except json.JSONDecodeError:
                raise Exception("Error parsing JSON content")
            
            json_content = dictionary
            
            file_data["content"] = json.dumps(json_content, indent=4)

            # Update the Gist content
            data = {
                "files": {
                    file_name: file_data
                }
            }
            update_response = requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data)

            if update_response.status_code == 200:
                print("Gist content updated successfully.")
            else:
                raise Exception("Failed to update Gist content")
        else:
            raise Exception("File not found in Gist")
    else:
        raise Exception("Failed to fetch Gist maybe wrong access token")