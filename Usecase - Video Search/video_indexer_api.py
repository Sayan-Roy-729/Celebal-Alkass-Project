# Azure Video Indexer Portal - https://api-portal.videoindexer.ai/
# Documentation - https://learn.microsoft.com/en-us/azure/azure-video-indexer/video-indexer-use-apis

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class VideoIndexerClient:
    def __init__(self, account_id: str, subscription_key: str, indexer_location: str = "trial"):
        """
        Initialize the Video Indexer client.

        :param account_id: The Video Indexer account ID.
        :param subscription_key: The Video Indexer subscription key.
        :param indexer_location: The location of the indexer (default: "trial").
        """
        self.account_id = account_id
        self.subscription_key = subscription_key
        self.indexer_location = indexer_location
        self.access_token = self.get_access_token()

    def account_info(self):
        """
        Get information about the Video Indexer account.

        :return: A tuple containing the account information and HTTP status code.
        """
        url = f"https://api.videoindexer.ai/{self.indexer_location}/Accounts/{self.account_id}?includeUsage=true&includeAmsInfo=true&includeStatistics=true&accessToken={self.access_token}"
        result = requests.get(url)

        if result.status_code == 200:
            return result.json(), result.status_code
        else:
            return {"error": "Account info failed", "response": result.json()}, result.status_code

    def get_access_token(self) -> str:
        """
        Get an access token for the Video Indexer API that can be used later for requesting other details.

        :return: The access token as a string.
        """
        url = f"https://api.videoindexer.ai/Auth/{self.indexer_location}/Accounts/{self.account_id}/AccessToken?allowEdit=true"
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key
        }
        result = requests.get(url, headers=headers)
        return result.text.replace('"', "")

    def upload_index_video(self, video_path: str, video_name: str = None):
        """
        Upload a video to create the index of it.

        :param video_path: The path to the video file.
        :return: A tuple containing the response and HTTP status code.
        """
        try:
            url = f"https://api.videoindexer.ai/{self.indexer_location}/Accounts/{self.account_id}/Videos?privacy=Private&name={video_name}&language=auto&accessToken={self.access_token}"

            headers = {
                "Cache-Control": "no-cache",
                "Ocp-Apim-Subscription-Key": self.subscription_key,
            }

            if video_path.startswith("http"):
                file_name = "".join(video_name.split(".")[:-1])
                blob_uri_url = f"{url}&videoUrl={video_path}&fileName={file_name}"
                response = requests.post(blob_uri_url, headers=headers)
            else:
                with open(video_path, 'rb') as file:
                    files = {'file': ('file', file, 'application/octet-stream')}
                    response = requests.post(url, headers=headers, files=files)

            if response.status_code == 200:
                return response.json(), response.status_code
            else:
                return {"error": "Video upload failed", "response": response.json()}, response.status_code
        except Exception as e:
            return {"error": str(e)}, response.status_code

    def get_video_index(self, video_id: str):
        """
        Get the index information for a video.

        :param video_id: The ID of the video.
        :return: A tuple containing the video index information and HTTP status code.
        """
        url = f"https://api.videoindexer.ai/{self.indexer_location}/Accounts/{self.account_id}/Videos/{video_id}/Index?language=English&reTranslate=false&includeStreamingUrls=true&includeSummarizedInsights=true&accessToken={self.access_token}"
        headers = {
            "Cache-Control": "no-cache",
            "Ocp-Apim-Subscription-Key": self.subscription_key,
        }
        result = requests.get(url, headers=headers)
        if result.status_code == 200:
            return result.json(), result.status_code
        else:
            return {"error": "Video indexing failed", "response": result.json()}, result.status_code

    def get_list_of_videos(self, page_size: int = 25, skip: int = 0):
        """
        Get a list of videos from the Azure Video Indexer account.

        :param page_size: The number of videos to retrieve per page (default: 25).
        :param skip: The number of videos to skip (default: 0).

        :return: A tuple containing the list of videos and HTTP status code.
        """
        url = f"https://api.videoindexer.ai/{self.indexer_location}/Accounts/{self.account_id}/Videos?pageSize={page_size}&skip={skip}&accessToken={self.access_token}"
        headers = {
            "Cache-Control": "no-cache",
            "Ocp-Apim-Subscription-Key": self.subscription_key,
        }
        result = requests.get(url, headers=headers)
        if result.status_code == 200:
            return result.json(), result.status_code
        else:
            return {"error": "Video indexing failed", "response": result.json()}, result.status_code


if __name__ == "__main__":
    account_id = os.getenv("ACCOUNT_ID")
    subscription_primary_key = os.getenv("SUBSCRIPTION_PRIMARY_KEY")
    video_indexer_location = os.getenv("VIDEO_INDEXER_LOCATION")

    # access_token = get_access_token(account_id, subscription_primary_key)

    # # video_path = "./Videos/Argentina v France _ FIFA World Cup Qatar 2022 Highlights.mp4"
    # # response_text, response_status_code = upload_index_video(
    # #     account_id=account_id,
    # #     subscription_key=subscription_primary_key,
    # #     video_path=video_path,
    # #     access_token=access_token
    # # )
    # # print(response_text)

    # video_id = "426374645c"
    # response_text, response_status_code = get_video_index(
    #     indexer_location = video_indexer_location,
    #     account_id       = account_id,
    #     subscription_key = subscription_primary_key,
    #     video_id         = video_id,
    #     access_token     = access_token
    # )
    # print(response_text)
    az_video_indexer = VideoIndexerClient(
        account_id=account_id,
        subscription_key=subscription_primary_key,
        indexer_location=video_indexer_location
    )
    response = az_video_indexer.upload_index_video(
        video_path="./Videos/argentina-vs-france-final-penalties-5usol1yr-16rdpyqc_WpdDMi6L.mp4")
    print(response)
