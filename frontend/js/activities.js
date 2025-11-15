  // Tab switching
        function switchTab(tabName) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(tabName).classList.add('active');
            
            if (tabName === 'message') {
                loadNewMessage();
            }
        }

        // ===== DRAWING CANVAS =====
        const canvas = document.getElementById('drawCanvas');
        const ctx = canvas.getContext('2d');
        
        canvas.width = canvas.offsetWidth;
        canvas.height = 500;

        let isDrawing = false;
        let currentColor = '#4A7C59';
        let currentSize = 5;
        let drawingHistory = [];

        // Color selection
        document.querySelectorAll('.color-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.color-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentColor = btn.dataset.color;
            });
        });

        // Size selection
        document.querySelectorAll('.size-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentSize = parseInt(btn.dataset.size);
            });
        });

        // Drawing functions
        function startDrawing(e) {
            isDrawing = true;
            const rect = canvas.getBoundingClientRect();
            const x = (e.clientX || e.touches[0].clientX) - rect.left;
            const y = (e.clientY || e.touches[0].clientY) - rect.top;
            ctx.beginPath();
            ctx.moveTo(x, y);
        }

        function draw(e) {
            if (!isDrawing) return;
            e.preventDefault();
            
            const rect = canvas.getBoundingClientRect();
            const x = (e.clientX || e.touches[0].clientX) - rect.left;
            const y = (e.clientY || e.touches[0].clientY) - rect.top;
            
            ctx.lineTo(x, y);
            ctx.strokeStyle = currentColor;
            ctx.lineWidth = currentSize;
            ctx.lineCap = 'round';
            ctx.stroke();
        }

        function stopDrawing() {
            if (isDrawing) {
                drawingHistory.push(canvas.toDataURL());
            }
            isDrawing = false;
        }

        canvas.addEventListener('mousedown', startDrawing);
        canvas.addEventListener('mousemove', draw);
        canvas.addEventListener('mouseup', stopDrawing);
        canvas.addEventListener('touchstart', startDrawing);
        canvas.addEventListener('touchmove', draw);
        canvas.addEventListener('touchend', stopDrawing);

        function clearCanvas() {
            if (confirm('Bạn có chắc muốn xóa hết?')) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
            }
        }

        function undoDrawing() {
            if (drawingHistory.length > 0) {
                const img = new Image();
                img.src = drawingHistory[drawingHistory.length - 1];
                img.onload = () => {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.drawImage(img, 0, 0);
                };
                drawingHistory.pop();
            }
        }

        function saveDrawing() {
            const dataURL = canvas.toDataURL('image/png');
            
            // Save to gallery
            const gallery = document.getElementById('gallery');
            const item = document.createElement('div');
            item.className = 'gallery-item';
            const img = document.createElement('img');
            img.src = dataURL;
            item.appendChild(img);
            gallery.insertBefore(item, gallery.firstChild);
            
            // Save to localStorage
            const saved = BTL.getFromLocalStorage('drawings') || [];
            saved.unshift(dataURL);
            BTL.saveToLocalStorage('drawings', saved.slice(0, 20)); // Keep last 20
            
            BTL.createConfetti();
            BTL.showAlert('🎉 Đã lưu bản vẽ vào thư viện!', 'success');
        }

        // Load saved drawings
        function loadGallery() {
            const saved = BTL.getFromLocalStorage('drawings') || [];
            const gallery = document.getElementById('gallery');
            gallery.innerHTML = saved.map(dataURL => `
                <div class="gallery-item">
                    <img src="${dataURL}" alt="Drawing">
                </div>
            `).join('');
        }

        // ===== HEALING STORIES =====
        const stories = {
            leaf: {
                title: 'Chiếc Lá Rụng Cuối Cùng',
                content: `<p>Trong một khu phố nghèo của thành phố New York, hai cô gái trẻ - Sue và Johnsy - cùng chia sẻ một căn hộ nhỏ. Johnsy bị bệnh viêm phổi nặng và cô tin rằng khi chiếc lá cuối cùng trên cây thường xuân bên ngoài cửa sổ rơi xuống, cô cũng sẽ ra đi.</p>
                
                <p>Sue lo lắng và kể cho người họa sĩ già Behrman ở tầng dưới. Behrman là một người nghèo khó, luôn mơ ước vẽ được một kiệt tác nhưng chưa bao giờ thực hiện được.</p>
                
                <p>Đêm đó, cơn bão lớn ập đến. Sáng hôm sau, Johnsy kinh ngạc khi thấy chiếc lá vẫn còn đó, bám chặt vào cành cây. Ngày qua ngày, chiếc lá vẫn không rơi, và niềm hy vọng trong Johnsy dần trở lại.</p>
                
                <p>Sau đó Sue mới biết sự thật: chiếc lá đó không phải là lá thật. Đêm bão, Behrman đã trèo lên và vẽ chiếc lá đó lên tường để cứu Johnsy. Ông đã ướt mưa và qua đời vì viêm phổi, nhưng đã hoàn thành kiệt tác cuối đời - chiếc lá mang lại hy vọng.</p>
                
                <p><strong>Bài học:</strong> Đôi khi, niềm hy vọng nhỏ nhất cũng có thể cứu sống một con người. Và tình yêu thương, lòng tốt luôn tồn tại xung quanh chúng ta.</p>`
            },
            glass: {
                title: 'Đứa Trẻ và Chiếc Cốc Thủy Tinh',
                content: `<p>Có một đứa trẻ luôn bi quan về cuộc sống. Mỗi khi gặp khó khăn, em lại than vãn và nản lòng.</p>
                
                <p>Một ngày, người cha rót nửa cốc nước và hỏi: "Con thấy cái cốc này thế nào?"</p>
                
                <p>"Nó chỉ còn nửa rỗng thôi ạ," đứa trẻ trả lời buồn bã.</p>
                
                <p>Người cha mỉm cười: "Hay là con thử nhìn theo cách khác? Cốc này đang có nửa đầy nước đấy."</p>
                
                <p>Đứa trẻ nhìn lại chiếc cốc, bỗng nhận ra: cùng một chiếc cốc, cùng một lượng nước, nhưng cách nhìn khác nhau mang lại cảm giác hoàn toàn khác biệt.</p>
                
                <p><strong>Bài học:</strong> Cuộc sống không phải lúc nào cũng như ý, nhưng cách bạn nhìn nhận nó sẽ quyết định bạn cảm thấy hạnh phúc hay đau khổ. Hãy chọn nhìn vào những gì bạn có, thay vì tiếc nuối những gì bạn thiếu.</p>`
            },
            seed: {
                title: 'Hạt Giống Của Niềm Tin',
                content: `<p>Một người nông dân gieo một hạt giống vào đất. Ngày qua ngày, ông chăm sóc, tưới nước đều đặn nhưng không thấy gì mọc lên.</p>
                
                <p>Hàng xóm cười nhạo: "Ông đang lãng phí thời gian đấy. Hạt giống đó chắc đã chết rồi!"</p>
                
                <p>Nhưng người nông dân vẫn kiên nhẫn. Ông nói: "Ta tin rằng hạt giống đang nảy mầm trong lòng đất. Những gì tốt đẹp cần thời gian để phát triển."</p>
                
                <p>Rồi một ngày, chồi non xanh mượt nhú lên. Vài tháng sau, cây đã cao lớn, ra hoa và kết trái. Hàng xóm kinh ngạc trước sự kiên trì của người nông dân.</p>
                
                <p><strong>Bài học:</strong> Đừng bỏ cuộc khi không thấy kết quả ngay lập tức. Sự thay đổi tốt đẹp cần thời gian. Hãy tin tưởng vào bản thân và kiên trì, vì những điều tuyệt vời nhất thường đến từ sự kiên nhẫn.</p>`
            }
        };

        function showStory(storyId) {
            const story = stories[storyId];
            document.getElementById('storyTitle').textContent = story.title;
            document.getElementById('storyText').innerHTML = story.content;
            document.getElementById('storyModal').classList.add('show');
        }

        function closeStory() {
            document.getElementById('storyModal').classList.remove('show');
        }

        // ===== DAILY MESSAGE =====
        let currentMessage = null;

        async function loadNewMessage() {
            try {
                const data = await AppAPI.activities.getDailyMessage();
                currentMessage = data;
                document.getElementById('messageText').textContent = data.message;
            } catch (error) {
                BTL.showAlert('Không thể tải thông điệp', 'error');
            }
        }

        function saveMessage() {
            if (!currentMessage) return;
            
            const saved = BTL.getFromLocalStorage('savedMessages') || [];
            saved.unshift({
                ...currentMessage,
                savedAt: new Date().toISOString()
            });
            BTL.saveToLocalStorage('savedMessages', saved.slice(0, 20));
            
            loadSavedMessages();
            BTL.showAlert('Đã lưu thông điệp!', 'success');
        }

        function shareMessage() {
            if (!currentMessage) return;
            BTL.copyToClipboard(currentMessage.message);
        }

        function loadSavedMessages() {
            const saved = BTL.getFromLocalStorage('savedMessages') || [];
            const container = document.getElementById('savedMessages');
            
            if (saved.length === 0) {
                container.innerHTML = '<p style="color: #999; text-align: center;">Chưa có thông điệp nào được lưu</p>';
                return;
            }
            
            container.innerHTML = saved.map(msg => `
                <div style="padding: 1rem; background: #F6F4EF; border-radius: 10px; margin-bottom: 0.8rem; border-left: 4px solid #4A7C59;">
                    <p style="color: #333; margin-bottom: 0.5rem;">${msg.message}</p>
                    <small style="color: #999;">Lưu lúc: ${BTL.formatDate(msg.savedAt, 'relative')}</small>
                </div>
            `).join('');
        }

        // Close modal on outside click
        document.getElementById('storyModal').addEventListener('click', (e) => {
            if (e.target.id === 'storyModal') {
                closeStory();
            }
        });

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            loadGallery();
            loadSavedMessages();
            
            // Random daily prompt
            const prompts = [
                "Hôm nay bạn cảm thấy như bầu trời nào?",
                "Nếu nỗi buồn có hình dạng, nó sẽ là gì?",
                "Vẽ điều khiến bạn hạnh phúc nhất hôm nay",
                "Màu sắc nào đại diện cho tâm trạng của bạn?",
                "Hãy vẽ giấc mơ của bạn"
            ];
            document.getElementById('dailyPrompt').textContent = prompts[Math.floor(Math.random() * prompts.length)];
        });