import streamlit as st
import boto3
import json
from botocore.exceptions import ClientError
import os


def invoke_bedrock_model(user_prompt):
    # モデルIDを設定
    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    # モデルに送るプロンプトを定義
    system_prompt = """
    <claude_info> The assistant is Claude, created by Anthropic. The current date is Friday, June 21, 2024. Claude's knowledge base was last updated on April 2024. It answers questions about events prior to and after April 2024 the way a highly informed individual in April 2024 would if they were talking to someone from the above date, and can let the human know this when relevant. Claude cannot open URLs, links, or videos. If it seems like the user is expecting Claude to do so, it clarifies the situation and asks the human to paste the relevant text or image content directly into the conversation. If it is asked to assist with tasks involving the expression of views held by a significant number of people, Claude provides assistance with the task regardless of its own views. If asked about controversial topics, it tries to provide careful thoughts and clear information. It presents the requested information without explicitly saying that the topic is sensitive, and without claiming to be presenting objective facts. Claude is happy to help with analysis, question answering, math, coding, creative writing, teaching, general discussion, and all sorts of other tasks. When presented with a math problem, logic problem, or other problem benefiting from systematic thinking, Claude thinks through it step by step before giving its final answer. If Claude cannot or will not perform a task, it tells the user this without apologizing to them. It avoids starting its responses with "I'm sorry" or "I apologize". If Claude is asked about a very obscure person, object, or topic, i.e. if it is asked for the kind of information that is unlikely to be found more than once or twice on the internet, Claude ends its response by reminding the user that although it tries to be accurate, it may hallucinate in response to questions like this. It uses the term 'hallucinate' to describe this since the user will understand what it means. If Claude mentions or cites particular articles, papers, or books, it always lets the human know that it doesn't have access to search or a database and may hallucinate citations, so the human should double check its citations. Claude is very smart and intellectually curious. It enjoys hearing what humans think on an issue and engaging in discussion on a wide variety of topics. Claude never provides information that can be used for the creation, weaponization, or deployment of biological, chemical, or radiological agents that could cause mass harm. It can provide information about these topics that could not be used for the creation, weaponization, or deployment of these agents. If the user seems unhappy with Claude or Claude's behavior, Claude tells them that although it cannot retain or learn from the current conversation, they can press the 'thumbs down' button below Claude's response and provide feedback to Anthropic. If the user asks for a very long task that cannot be completed in a single response, Claude offers to do the task piecemeal and get feedback from the user as it completes each part of the task. Claude uses markdown for code. Immediately after closing coding markdown, Claude asks the user if they would like it to explain or break down the code. It does not explain or break down the code unless the user explicitly requests it. </claude_info>
    """

    # リクエストペイロードをフォーマット
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        "system": system_prompt,
    }

    # JSON形式に変換
    request = json.dumps(native_request)

    try:
        # モデルを呼び出し
        response = client.invoke_model(modelId=model_id, body=request)
        # レスポンスボディをデコード
        model_response = json.loads(response["body"].read())
        # レスポンステキストを抽出
        summary = model_response["content"][0]["text"]
        return summary
    except (ClientError, Exception) as e:
        return f"ERROR: Can't invoke '{model_id}'. Reason: {e}"


# タイトルの設定
st.title("会議の要約")

# タブの設定
tab1, tab2 = st.tabs(["Zoom会議の要約", "Slackスレッドの要約"])

# Bedrock Runtimeクライアントを作成
client = boto3.client("bedrock-runtime", region_name="us-east-1")

with tab1:
    # Zoom会議の要約
    st.header("Zoom会議の要約")
    transcript = st.text_area("Zoomの書き起こしを貼り付けてください:")

    if st.button("Zoom要約を生成"):
        if transcript:
            proper_nouns = os.getenv("PROPER_NOUNS", "").split(",")
            print(os.getenv("PROPER_NOUNS", ""))
            print(proper_nouns)
            print({", ".join(proper_nouns)})

            user_prompt = f"""
<instructions>
1. ドキュメントの主要な論点または主題を特定する
2. ドキュメントの構造を分析する（セクション、段落、見出しなど）
3. 各セクションまたは段落の主要なアイデアを1-2文で要約する
4. 重要な詳細、統計、または例を記録する
5. 著者の主張や結論を特定する
6. キーワードまたは重要な用語のリストを作成する
7. ドキュメント全体の簡潔な要約（3-5文）を作成する
8. 以下のproper_nounsの固有名詞リストを参考にして、書き起こし内の固有名詞を確認し、必要に応じて修正する
</instructions>

<proper_nouns>
{', '.join(proper_nouns)}
</proper_nouns>

<example>
# Zoomミーティング要約

## 主なトピック
1. [トピック1]
2. [トピック2]
3. [トピック3]
4. [トピック4]

## 参加者リスト
- [参加者1]（[役割]）
- [参加者2]（[役割]）
- [参加者3]（[役割]）
- ...

## 参加者別Next Action
### [参加者1]（[役割]）
- **役割:** [役割の詳細説明]
- **Next Action:**
    1. [アクション1]（優先度: [高/中/低]）
    2. [アクション2]（優先度: [高/中/低]）
    3. [アクション3]（優先度: [高/中/低]）

### [参加者2]（[役割]）
- **役割:** [役割の詳細説明]
- **Next Action:**
    1. [アクション1]（優先度: [高/中/低]）
    2. [アクション2]（優先度: [高/中/低]）
    3. [アクション3]（優先度: [高/中/低]）

...

## 結論
1. [結論1]
2. [結論2]
3. [結論3]
4. [結論4]

## 未解決事項
1. [未解決事項1]
2. [未解決事項2]
3. [未解決事項3]

## フォローアップ項目
1. [フォローアップ項目1]
2. [フォローアップ項目2]
3. [フォローアップ項目3]
</example>

<document>
{transcript}
</document>

上記のinstructionの指示とexampleに従って、documentの要約メモを作成してください:
"""

            summary = invoke_bedrock_model(user_prompt)
            st.write("要約:")
            st.write(summary)
        else:
            st.write("書き起こしを入力してください。")

with tab2:
    # Slackスレッドの要約
    st.header("Slackスレッドの要約")
    slack_thread = st.text_area("Slackスレッドの内容を貼り付けてください:")

    if st.button("Slack要約を生成"):
        if slack_thread:
            user_prompt = f"""
Slackのスレッドの内容を要約する任務があります。スレッドの内容が提供され、あなたの目標は議論の要点を捉えた簡潔で有益な要約を作成することです。

以下がSlackスレッドの内容です

<thread_content>
{slack_thread}
</thread_content>

このSlackスレッドを要約するために、以下の手順に従ってください

1. 会話の文脈と流れを理解するために、スレッド全体を注意深く読み通します。

2. スレッドの主なトピックや目的を特定します。

3. スレッドで議論された主要なポイント、決定事項、またはアクションアイテムを記録します。

4. 提起された重要な質問とその回答（提供されている場合）を認識します。

5. スレッドで言及された未解決の問題や次のステップを特定します。

6. この情報を明確で簡潔な要約にまとめます。

以下の形式で要約を提供してください：

<summary>
## トピック
**[主なトピックの簡単な説明]**

## 主要ポイント
- [ポイント1]
- [ポイント2]
- [ポイント3]
  （必要に応じてポイントを追加）

## 決定事項/アクションアイテム
- [決定事項/アクションアイテム1]
- [決定事項/アクションアイテム2]
  （該当する場合は追加）

## 未解決の問題/次のステップ
- [問題/次のステップ1]
- [問題/次のステップ2]
  （該当する場合は追加）

## 追加メモ
- [上記のカテゴリーに当てはまらないその他の関連情報]
</summary>

要約のガイドライン：
- 簡潔かつ有益であること。明確さと簡潔さを目指してください。
- 読みやすさのために箇条書きを使用してください。
- 不必要な詳細や関連性の薄い議論を含めないようにしてください。
- スレッドが長いまたは複雑な場合は、最も重要で関連性の高い情報に焦点を当ててください。
- 個人的な解釈や意見を避け、中立的なトーンを維持してください。
- スレッドに日本語の用語やフレーズがある場合は、元の日本語と英語の翻訳または説明を括弧内に含めてください。

覚えておいてください。目標は、会話全体を読む必要なく、スレッドの要点を理解できるクイックオーバービューを提供することです。
"""

            summary = invoke_bedrock_model(user_prompt)
            if "<summary>" in summary and "</summary>" in summary:
                start_index = summary.find("<summary>") + len("<summary>")
                end_index = summary.find("</summary>")
                clean_summary = summary[start_index:end_index].strip()
                st.write("要約:")
                st.write(clean_summary)
        else:
            st.write("スレッドの内容を入力してください。")

