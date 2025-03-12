import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { MessageCircle, X, Send, Bot } from "lucide-react";

const ChatBot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Hi! I'm a Medical AI Assistant. How can I help you today?", isUser: false }
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = { text: inputMessage, isUser: true };
    setMessages((prev) => [...prev, userMessage]);
    setInputMessage("");
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:5001/chat", {
        message: inputMessage
      });

      if (response.data.reply) {
        setMessages((prev) => [...prev, { text: response.data.reply, isUser: false }]);
      } else {
        setMessages((prev) => [...prev, { text: "Error: No response from AI", isUser: false }]);
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [...prev, { text: "Network error. Try again later.", isUser: false }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-8 right-8 z-50">
      {isOpen ? (
        <div className="w-80 h-[500px] bg-white rounded-2xl shadow-2xl flex flex-col border border-gray-100">
          {/* Header */}
          <div className="flex items-center justify-between p-4 bg-black/90 rounded-t-2xl">
            <div className="flex items-center gap-3">
              <Bot className="w-6 h-6 text-white" />
              <h3 className="text-white font-semibold">EM-Medic BOT</h3>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-white hover:text-gray-300 transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 p-4 overflow-y-auto space-y-4 bg-gray-50">
            {messages.map((message, index) => (
              <div key={index} className={`flex ${message.isUser ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[80%] rounded-2xl p-3 ${message.isUser ? "bg-black text-white" : "bg-white border border-gray-200"}`}>
                  <p className="text-sm">{message.text}</p>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-200 text-gray-700 rounded-2xl px-3 py-2 text-sm">Typing...</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-gray-100">
            <div className="flex gap-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
                placeholder="Type your message..."
                className="flex-1 rounded-xl px-4 py-2 text-sm border border-gray-200 focus:ring-2 focus:ring-black"
              />
              <button onClick={handleSendMessage} disabled={!inputMessage.trim() || loading} className="p-2 bg-black text-white rounded-xl hover:bg-gray-800">
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      ) : (
        <button onClick={() => setIsOpen(true)} className="w-14 h-14 bg-black rounded-full shadow-lg hover:bg-gray-800">
          <MessageCircle className="w-6 h-6 text-white" />
        </button>
      )}
    </div>
  );
};

export default ChatBot;
