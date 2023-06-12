const { Configuration, OpenAIApi } = require("openai")

const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

const query = async (prompt) => {

    const message= [
        {role: "assistant", content: "You are a teacher"},
        {role: "user", content: prompt}
    ]
    const completion = await openai.createChatCompletion({
        model: "gpt-3.5-turbo", messages: message, temperature: 0
    });
    console.log(completion.data.choices[0].message.content);
}

query("What is a macroprudential policy and what are the advantages?")
