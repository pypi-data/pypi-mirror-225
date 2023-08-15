import openai, time
from typing import List, Dict, Any, Optional
from utils.url_utils import URL, URLManager
from schema.schema_base_prompt import SystemMessage, UserMessage, PromptContext, ChatCompletionMessage, MessageRole, Message, ChatCompletionMessageNoFunctions
from chains.chain_generic import chat_complete


def take_cve_return_urls(cve_id: str) -> List[str]:
    """ 
    Take a CVE ID and return a list of URLs

    """
    return ["https://nvd.nist.gov/vuln/detail/" + cve_id, "https://www.cvedetails.com/cve/" + cve_id , "https://ubuntu.com/security/"+cve_id , "https://alas.aws.amazon.com/cve/html/" + cve_id + ".html"]

def run (cve_id: str) -> Dict :
    urls = take_cve_return_urls(cve_id)
    curls = URLManager(urls)
    paragraphs = []
    for i in range ( len (urls) ):
        time.sleep(2)
        urltext = curls.get_all_urls()[i].url + ": ".join ( curls.get_all_urls()[i].paragraphs )    
        paragraphs.append (urltext)
    return paragraphs