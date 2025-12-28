# AVS Guide: Setting up Web Research (Gemini + Google Search)

The AVS Toolkit uses the Gemini API to perform "The Information Hunt" for real-time web data. This allows your Value Stories to be grounded in current facts (like company headquarters or financial status) without manual searching.

## 1. Get your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google Account.
3. Click on "Get API key" in the sidebar.
4. Click "Create API key".
5. Important: Copy this key. You will need it for the Toolkit to function.

## 2. Setting the Key in your Environment

To keep your key secure, do not hardcode it into your Value Stories. Instead, the AVS Toolkit looks for an environment variable.

## Mac/Linux:

Add this to your `~/.zshrc` or `~/.bash_profile`:
```
export GEMINI_API_KEY="your_actual_key_here"
```

Then run `source ~/.zshrc`.

### Windows:

In PowerShell, run:
```
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'your_actual_key_here', 'User')
```

*Note: Restart your terminal after setting this.*

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

2. Type echo $GEMINI_API_KEY (Mac) or $env:GEMINI_API_KEY (Windows) in your terminal to ensure the computer can "see" the key.