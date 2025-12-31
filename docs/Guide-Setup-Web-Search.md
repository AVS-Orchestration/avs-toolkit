# AVS Guide: Setting up Web Research (Gemini + Google Search)

The AVS Toolkit uses the Gemini API to perform "The Information Hunt" for real-time web data. This allows your Value Stories to be grounded in current facts (like company headquarters or financial status) without manual searching.

## 1. Get your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google Account.
3. Click on "Get API key" in the sidebar.
4. Click "Create API key".
5. Important: Copy this key. You will need it for the Toolkit to function.

## 2. Setting the Key in your Environment (.env)

To keep your key secure and easy to manage, the AVS Toolkit looks for a file named `.env` in the project root.

1. Locate the file named `.env.template` in the AVS Toolkit folder.
2. Create a copy of it and rename the copy to `.env`.
3. Open `.env` in VS Code or any text editor.
4. Find the line `GEMINI_API_KEY="your_gemini_key_here"` and replace the placeholder with your actual key from Step 1.
5. Save the file.

**Note**: The `.env` file is hidden by default on many systems. In VS Code, it will be visible in the file explorer.

## 3. Usage in a Value Story

Simply add a search_query to any item in your context_manifest:

context_manifest:
  - key: "company_research"
    description: "Fetch live data about the target employer."
    search_query: "NVIDIA corporation headquarters, employee count, and 2024 revenue"


## 4. Cost and Limits

As of late 2025, using the `gemini-2.5-flash` model is **Free of Charge** within the following limits:

**Rate Limit**: 15 Requests Per Minute.

**Volume**: 1,500 Requests Per Day.

**Data Privacy**: In the Free Tier, Google may use your inputs to improve their models. If you are handling highly sensitive corporate data, consider enabling the Pay-as-you-go tier, where data is not used for training.

## 5. Troubleshooting

If you see an "Authentication Error" during the `assemble` phase:

1. Verify your API key is active in AI Studio.
2. Ensure your `.env` file is saved in the root of the `avs-value-story` folder.
3. Ensure the key is inside quotes: `GEMINI_API_KEY="AIza..."`.