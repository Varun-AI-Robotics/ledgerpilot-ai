import {
  Bot,
  Send,
  Sparkles,
  User,
} from "lucide-react";

import { useState } from "react";
import { askAI } from "../services/api";

function AIAssistant() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const suggestions = [
    "Show me all high priority exceptions",
    "Why did the match rate decrease?",
    "Explain the missing settlements",
    "What needs attention first?",
  ];

  const sendQuestion = async (text = question) => {
    if (!text.trim() || loading) return;

    const userMessage = text.trim();

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: userMessage,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const result = await askAI(userMessage);

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: result.answer || result.response || result,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "I couldn't complete that analysis. Please check the backend and Gemini connection.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fade-in h-[calc(100vh-7rem)] flex flex-col">
      {/* Intro */}
      {messages.length === 0 && (
        <div className="flex-1 flex flex-col items-center justify-center text-center">
          <div className="w-16 h-16 rounded-2xl bg-[#111315] text-white flex items-center justify-center mb-5">
            <Bot size={28} />
          </div>

          <div className="flex items-center gap-2 text-xs text-gray-400">
            <Sparkles size={14} />
            LedgerPilot AI
          </div>

          <h1 className="text-3xl font-bold text-gray-900 mt-3">
            Your finance operations copilot
          </h1>

          <p className="text-sm text-gray-500 max-w-xl mt-3">
            Ask questions about reconciliation results,
            exceptions, settlements and financial controls.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-8 max-w-2xl w-full">
            {suggestions.map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => sendQuestion(suggestion)}
                className="text-left p-4 bg-white border border-gray-200 rounded-xl hover:border-gray-400 hover:shadow-sm transition"
              >
                <p className="text-sm font-medium text-gray-700">
                  {suggestion}
                </p>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Messages */}
      {messages.length > 0 && (
        <div className="flex-1 overflow-y-auto max-w-4xl w-full mx-auto px-2 pb-5">
          <div className="space-y-5">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex gap-3 ${
                  message.role === "user"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >
                {message.role === "ai" && (
                  <div className="w-9 h-9 shrink-0 rounded-xl bg-[#111315] text-white flex items-center justify-center">
                    <Bot size={17} />
                  </div>
                )}

                <div
                  className={`
                    max-w-[75%]
                    px-4
                    py-3
                    rounded-2xl
                    text-sm
                    leading-6
                    ${
                      message.role === "user"
                        ? "bg-[#111315] text-white rounded-br-md"
                        : "bg-white border border-gray-200 text-gray-700 rounded-bl-md"
                    }
                  `}
                >
                  {message.text}
                </div>

                {message.role === "user" && (
                  <div className="w-9 h-9 shrink-0 rounded-xl bg-gray-200 flex items-center justify-center">
                    <User size={17} />
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex gap-3">
                <div className="w-9 h-9 rounded-xl bg-[#111315] text-white flex items-center justify-center">
                  <Bot size={17} />
                </div>

                <div className="bg-white border border-gray-200 rounded-2xl px-5 py-4">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:150ms]" />
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:300ms]" />
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="max-w-4xl w-full mx-auto">
        <div className="bg-white border border-gray-300 rounded-2xl p-2 shadow-sm flex items-center">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendQuestion();
              }
            }}
            placeholder="Ask about your financial operations..."
            className="flex-1 px-4 py-3 outline-none text-sm"
          />

          <button
            onClick={() => sendQuestion()}
            disabled={!question.trim() || loading}
            className="w-11 h-11 rounded-xl bg-[#111315] text-white flex items-center justify-center disabled:opacity-30 transition"
          >
            <Send size={17} />
          </button>
        </div>

        <p className="text-[10px] text-center text-gray-400 mt-2">
          LedgerPilot AI answers using your reconciliation data.
        </p>
      </div>
    </div>
  );
}

export default AIAssistant;