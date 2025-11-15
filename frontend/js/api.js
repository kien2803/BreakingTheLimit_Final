// API SERVICE

const MockAPI = {
    delay: (ms = 1000) => new Promise(resolve => setTimeout(resolve, ms)),
    
    auth: {
        async login(email, password) {
            await MockAPI.delay();
            const user = {
                id: 1,
                name: 'Nguyễn Văn A',
                email: email,
                role: 'student'
            };
            const token = 'mock_token_' + Date.now();
            localStorage.setItem('authToken', token);
            localStorage.setItem('currentUser', JSON.stringify(user));
            return { token, user };
        }
    },
    
    journal: {
        async create(journalData) {
            await MockAPI.delay();
            return {
                id: Date.now(),
                ...journalData,
                date: new Date().toISOString()
            };
        },
        
        async getAll() {
            await MockAPI.delay();
            return [
                {
                    id: 1,
                    date: new Date().toISOString(),
                    content: 'Hôm nay em cảm thấy vui vẻ...',
                    mood: 'happy'
                }
            ];
        }
    },
    
    ai: {
        async analyzeEmotion(text, mood) {
            await MockAPI.delay(2000);
            return {
                emotionScore: {
                    positive: Math.random() * 40 + 50,
                    neutral: Math.random() * 30 + 10,
                    negative: Math.random() * 20
                },
                wellnessScore: Math.floor(Math.random() * 30 + 60),
                suggestions: [
                    'Hãy nghe một bản nhạc nhẹ nhàng',
                    'Thử viết 3 điều bạn biết ơn hôm nay',
                    'Đi dạo 10 phút ngoài trời'
                ]
            };
        }
    },
    
    activities: {
        async getDailyMessage() {
            await MockAPI.delay();
            const messages = [
                'Hít thật sâu, thở ra từ từ, bạn xứng đáng được bình yên.',
                'Mỗi ngày là một khởi đầu mới, hãy tin vào bản thân.',
                'Bạn mạnh mẽ hơn bạn nghĩ!'
            ];
            return {
                id: Date.now(),
                message: messages[Math.floor(Math.random() * messages.length)]
            };
        }
    }
};

window.AppAPI = MockAPI;