import { useEffect, useMemo, useState } from 'react';
import { NavLink, Route, Routes, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, BrainCircuit, BookOpenText, Code2, Database, FolderUp, Gauge, MessageSquareText, MoonStar, Rocket, Search, Settings2, Sparkles, Upload, Wand2 } from 'lucide-react';
import { fetchHealth, fetchModels, sendChat, uploadDocument, listDocuments } from './services/api';

type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
};

const navItems = [
  { label: 'Home', to: '/', icon: Rocket },
  { label: 'Chat', to: '/chat', icon: MessageSquareText },
  { label: 'Knowledge Base', to: '/knowledge', icon: BookOpenText },
  { label: 'Upload Documents', to: '/knowledge', icon: Upload },
  { label: 'Code Explanation', to: '/chat', icon: Code2 },
  { label: 'Debugging Assistant', to: '/chat', icon: Sparkles },
  { label: 'Practice & Learn', to: '/chat', icon: BrainCircuit },
  { label: 'Interview Preparation', to: '/chat', icon: Gauge },
  { label: 'Conversation History', to: '/chat', icon: Database },
  { label: 'Model Settings', to: '/models', icon: Settings2 },
  { label: 'System Status', to: '/models', icon: Wand2 },
];

function Sidebar() {
  return (
    <aside className="hidden lg:flex w-72 flex-col border-r border-white/10 bg-slate-950/60 p-5 backdrop-blur-xl">
      <div className="mb-8 flex items-center gap-3">
        <div className="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-violet-500 to-blue-500 shadow-lg shadow-indigo-500/30">
          <Code2 className="h-5 w-5 text-white" />
        </div>
        <div>
          <h1 className="text-lg font-semibold text-white">AI Coding Assistant</h1>
          <p className="text-xs text-slate-400">RAG workspace</p>
        </div>
      </div>

      <nav className="space-y-2 text-sm">
        {navItems.map(({ label, to, icon: Icon }) => (
          <NavLink
            key={label}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-xl px-3 py-2.5 transition ${
                isActive ? 'bg-indigo-500/15 text-white ring-1 ring-indigo-400/40' : 'text-slate-300 hover:bg-slate-800/80 hover:text-white'
              }`
            }
          >
            <Icon className="h-4 w-4" />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="mt-auto rounded-2xl border border-indigo-500/30 bg-indigo-500/10 p-4 text-xs text-slate-200">
        <div className="mb-2 flex items-center justify-between">
          <span className="text-slate-300">Active LLM</span>
          <span className="font-medium text-indigo-200">qwen2.5:3b</span>
        </div>
        <div className="mb-2 flex items-center justify-between">
          <span className="text-slate-300">Embedding</span>
          <span className="font-medium text-cyan-200">nomic-embed-text</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-slate-300">Ollama</span>
          <span className="rounded-full bg-emerald-500/15 px-2 py-1 font-medium text-emerald-300">Online</span>
        </div>
      </div>
    </aside>
  );
}

function DashboardPage() {
  const navigate = useNavigate();
  const quickActions = [
    { label: 'Explain Code', icon: Code2, action: () => navigate('/chat') },
    { label: 'Debug Code', icon: Sparkles, action: () => navigate('/chat') },
    { label: 'Practice Coding', icon: BrainCircuit, action: () => navigate('/chat') },
    { label: 'Prepare for Interviews', icon: Gauge, action: () => navigate('/chat') },
  ];

  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="overflow-hidden rounded-3xl border border-white/10 bg-slate-900/70 shadow-2xl shadow-indigo-950/20">
        <div className="relative flex min-h-[260px] flex-col justify-end bg-cover bg-center p-8" style={{ backgroundImage: "linear-gradient(135deg, rgba(6,10,22,0.7), rgba(10,17,34,0.95)), url('/images/mountain-hero.jpg')" }}>
          <div className="absolute inset-0 bg-gradient-to-r from-slate-950/60 via-slate-900/30 to-indigo-950/50" />
          <div className="relative z-10 max-w-2xl">
            <p className="mb-3 text-sm uppercase tracking-[0.22em] text-indigo-200/90">AI Coding Companion</p>
            <h2 className="text-4xl font-bold text-white">AI Coding Assistant</h2>
            <p className="mt-3 text-lg text-slate-200">Learn, Debug, Practice, and Master Programming with RAG.</p>
          </div>
        </div>
      </motion.div>

      <div className="grid gap-4 lg:grid-cols-[1.5fr_0.9fr]">
        <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-5">
          <label className="mb-3 block text-xs font-medium uppercase tracking-[0.2em] text-slate-400">Ask a programming question</label>
          <div className="flex gap-3">
            <input className="flex-1 rounded-2xl border border-slate-700 bg-slate-950/80 px-4 py-3 text-slate-100 outline-none ring-0 placeholder:text-slate-500 focus:border-indigo-500" placeholder="Ask about Python, debugging, interview prep, or code explanations..." />
            <button onClick={() => navigate('/chat')} className="rounded-2xl bg-gradient-to-r from-indigo-500 to-blue-500 px-5 py-3 font-medium text-white shadow-lg shadow-indigo-500/30 transition hover:scale-[1.02]">Send</button>
          </div>
        </div>

        <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-5">
          <div className="mb-3 flex items-center justify-between">
            <p className="text-sm font-medium text-slate-200">Active model</p>
            <span className="rounded-full border border-emerald-500/40 bg-emerald-500/10 px-2 py-1 text-xs text-emerald-300">Online</span>
          </div>
          <div className="space-y-2 text-sm text-slate-300">
            <p><span className="text-slate-400">Generation:</span> qwen2.5:3b</p>
            <p><span className="text-slate-400">Embedding:</span> nomic-embed-text</p>
            <p><span className="text-slate-400">Context:</span> Local RAG pipeline</p>
          </div>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {quickActions.map(({ label, icon: Icon, action }) => (
          <button key={label} onClick={action} className="group rounded-2xl border border-white/10 bg-slate-900/70 p-4 text-left transition hover:border-indigo-500/30 hover:bg-slate-900">
            <div className="mb-3 inline-flex rounded-xl bg-indigo-500/10 p-2 text-indigo-200 group-hover:bg-indigo-500/20">
              <Icon className="h-5 w-5" />
            </div>
            <p className="text-base font-medium text-white">{label}</p>
            <div className="mt-4 flex items-center gap-2 text-xs text-slate-400">
              Open workspace <ArrowRight className="h-3.5 w-3.5" />
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([{
    id: 'welcome',
    role: 'assistant',
    content: 'Welcome to the AI Coding Assistant. Ask me about Python, debugging, code explanations, or interview prep.',
  }]);
  const [input, setInput] = useState('Explain Python list comprehensions with an example.');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    setLoading(true);
    setError('');
    const userMessage: Message = { id: Date.now().toString(), role: 'user', content: trimmed };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');

    try {
      const response = await sendChat({ question: trimmed, conversation_id: 'demo-chat', selected_model: 'qwen2.5:3b' });
      const assistantMessage: Message = { id: Date.now().toString() + '-assistant', role: 'assistant', content: response.answer || 'No answer returned.' };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate response.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-full flex-col rounded-3xl border border-white/10 bg-slate-900/70 p-4">
      <div className="mb-4 flex items-center justify-between border-b border-white/10 pb-3">
        <div>
          <h3 className="text-xl font-semibold text-white">Programming Chat</h3>
          <p className="text-sm text-slate-400">Grounded Q&A with local RAG and Ollama</p>
        </div>
        <div className="rounded-full border border-indigo-500/30 bg-indigo-500/10 px-3 py-1 text-xs text-indigo-200">qwen2.5:3b</div>
      </div>

      <div className="flex-1 space-y-3 overflow-y-auto pr-1">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-3xl rounded-2xl px-4 py-3 ${message.role === 'user' ? 'bg-indigo-500 text-white' : 'border border-white/10 bg-slate-950/70 text-slate-100'}`}>
              <p className="whitespace-pre-wrap text-sm leading-7">{message.content}</p>
            </div>
          </div>
        ))}
        {loading && <div className="text-sm text-slate-400">Generating answer...</div>}
        {error && <div className="rounded-xl border border-red-500/40 bg-red-500/10 px-3 py-2 text-sm text-red-300">{error}</div>}
      </div>

      <div className="mt-4 rounded-2xl border border-white/10 bg-slate-950/80 p-3">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          rows={4}
          className="w-full resize-none bg-transparent px-2 py-2 text-sm text-white outline-none placeholder:text-slate-500"
          placeholder="Ask a question..."
        />
        <div className="mt-3 flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <Search className="h-3.5 w-3.5" />
            RAG retrieval enabled
          </div>
          <button onClick={handleSend} disabled={loading} className="rounded-xl bg-gradient-to-r from-indigo-500 to-blue-500 px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-60">{loading ? 'Sending...' : 'Send'}</button>
        </div>
      </div>
    </div>
  );
}

function KnowledgeBasePage() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [status, setStatus] = useState('Ready');
  const [setError] = useState('');
  useEffect(() => {
    listDocuments().then((result) => setDocuments(result.documents || [])).catch(() => setStatus('Unable to fetch documents'));
  }, []);

  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    try {
      await uploadDocument(formData);
      const result = await listDocuments();
      setDocuments(result.documents || []);
      setStatus('Indexed successfully');
    } catch (err) {
      setStatus(err instanceof Error ? err.message : 'Upload failed');
    }
  };

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-5">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-xl font-semibold text-white">Knowledge Base</h3>
          <span className="rounded-full border border-emerald-500/40 bg-emerald-500/10 px-2 py-1 text-xs text-emerald-300">{status}</span>
        </div>
        <label className="flex cursor-pointer items-center justify-center gap-3 rounded-2xl border border-dashed border-indigo-500/40 bg-indigo-500/5 p-5 text-indigo-200 hover:border-indigo-400">
          <FolderUp className="h-5 w-5" />
          <span>Upload PDF, TXT, Markdown, or DOCX</span>
          <input type="file" className="hidden" onChange={handleUpload} />
        </label>
      </div>

      <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-5">
        <div className="mb-4 flex items-center justify-between">
          <h4 className="text-lg font-semibold text-white">Indexed Documents</h4>
          <p className="text-xs text-slate-400">{documents.length} files</p>
        </div>
        <div className="space-y-3">
          {documents.length === 0 ? (
            <p className="text-sm text-slate-400">No documents indexed yet.</p>
          ) : (
            documents.map((item: any) => (
              <div key={item.id} className="flex items-center justify-between rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3">
                <div>
                  <p className="font-medium text-white">{item.filename}</p>
                  <p className="text-xs text-slate-400">{item.file_type} • {item.chunk_count ?? 0} chunks</p>
                </div>
                <span className="rounded-full border border-cyan-500/30 bg-cyan-500/10 px-2 py-1 text-xs text-cyan-200">{item.status}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

function ModelSettingsPage() {
  const [models, setModels] = useState<string[]>([]);
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    fetchModels().then((data) => setModels(data.models || [])).catch(() => setModels([]));
    fetchHealth().then((data) => setHealth(data)).catch(() => setHealth(null));
  }, []);

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-5">
        <h3 className="text-xl font-semibold text-white">Model Settings</h3>
        <div className="mt-5 grid gap-4 md:grid-cols-2">
          <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-4">
            <p className="mb-2 text-xs uppercase tracking-[0.2em] text-slate-400">Generation model</p>
            <div className="flex items-center justify-between">
              <span className="text-lg font-medium text-white">qwen2.5:3b</span>
              <span className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2 py-1 text-xs text-emerald-200">Default</span>
            </div>
          </div>
          <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-4">
            <p className="mb-2 text-xs uppercase tracking-[0.2em] text-slate-400">Embedding model</p>
            <div className="flex items-center justify-between">
              <span className="text-lg font-medium text-white">nomic-embed-text</span>
              <span className="rounded-full border border-cyan-500/30 bg-cyan-500/10 px-2 py-1 text-xs text-cyan-200">Local</span>
            </div>
          </div>
        </div>
      </div>

      <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-5">
        <div className="mb-4 flex items-center justify-between">
          <h4 className="text-lg font-semibold text-white">Installed Ollama models</h4>
          <button className="rounded-xl border border-white/10 bg-slate-950/70 px-3 py-2 text-xs text-slate-200 hover:border-indigo-500/30">Refresh</button>
        </div>
        <div className="space-y-2">
          {models.length === 0 ? <p className="text-sm text-slate-400">No models detected. Start Ollama and run `ollama pull qwen2.5:3b`.</p> : models.map((model) => (
            <div key={model} className="flex items-center justify-between rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-sm text-slate-200">
              <span>{model}</span>
              {model === 'qwen2.5:3b' ? <span className="text-emerald-300">active</span> : <span className="text-slate-400">available</span>}
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-5 text-sm text-slate-300">
        <p className="text-slate-200">Ollama connection: {health?.ollama_connected ? 'Connected' : 'Unavailable'}</p>
        <p className="mt-2">Default generation model: {health?.active_model || 'qwen2.5:3b'}</p>
      </div>
    </div>
  );
}

function AppShell() {
  return (
    <div className="min-h-screen bg-[#07111F] text-slate-100">
      <div className="mx-auto flex max-w-[1600px] gap-6 p-4 lg:p-6">
        <Sidebar />
        <main className="flex-1">
          <header className="mb-6 flex flex-col gap-4 rounded-3xl border border-white/10 bg-slate-900/60 px-5 py-4 backdrop-blur-xl md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Workspace</p>
              <h2 className="text-2xl font-semibold text-white">AI Coding Assistant</h2>
            </div>
            <div className="flex items-center gap-3">
              <div className="rounded-xl border border-white/10 bg-slate-950/80 px-3 py-2 text-sm text-slate-200">Generation: qwen2.5:3b</div>
              <div className="rounded-xl border border-white/10 bg-slate-950/80 px-3 py-2 text-sm text-slate-200">Embedding: nomic-embed-text</div>
              <button className="rounded-xl border border-white/10 bg-slate-950/80 p-2 text-slate-200"><MoonStar className="h-4 w-4" /></button>
            </div>
          </header>

          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/knowledge" element={<KnowledgeBasePage />} />
            <Route path="/models" element={<ModelSettingsPage />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return <AppShell />;
}
