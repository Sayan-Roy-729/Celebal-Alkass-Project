import pandas as pd

from utils import ChatBotSummarizer


def main():
    # df = pd.read_csv("news_articles_data_2023.csv").query("news_id == 170541")
    # for _, row in df.iterrows():
    #     content = row.body
    df = pd.read_csv("news_articles_data_2023.csv")
    content = df.body[0]
    
    # response = LangchainSummarization(df.body[0]).summarize()
    # response = langchain_summarize(content)

    gpt, langchain = ChatBotSummarizer().chat_and_summarize(content)
    print(gpt, end="\n\n")
    print(langchain[:-10])

if __name__ == "__main__":
    main()
