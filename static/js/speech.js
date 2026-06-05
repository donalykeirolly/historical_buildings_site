
class TextToSpeech {
    constructor() {
        this.synth = window.speechSynthesis;
        this.isSpeaking = false;
        this.currentUtterance = null;
        this.rate = 0.9;
        this.pitch = 1;
        this.voice = null;
        this.hoverTimer = null;
        this.currentSpokenElement = null;
        
        this.init();
    }
    
    init() {
        if (this.synth) {
            this.loadVoices();
            if (speechSynthesis.onvoiceschanged !== undefined) {
                speechSynthesis.onvoiceschanged = () => this.loadVoices();
            }
        }
        
        this.addHoverSpeak();
        this.addFocusSpeak();
        this.addSpeechControls();
        
        console.log("🎤 Готово! Наводите мышку на любой элемент — он сразу озвучится.");
    }
    
    loadVoices() {
        this.voices = this.synth.getVoices();
        this.voice = this.voices.find(voice => voice.lang.includes('ru')) || this.voices[0];
    }
    
    speak(text, immediate = true) {
        if (!this.synth) {
            return;
        }

        text = this.cleanText(text);
        if (!text || text.length === 0) {
            return;
        }
        
        if (this.isSpeaking) {
            this.synth.cancel();
        }
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = this.rate;
        utterance.pitch = this.pitch;
        if (this.voice) utterance.voice = this.voice;
        utterance.lang = 'ru-RU';
        
        utterance.onstart = () => { 
            this.isSpeaking = true; 
        };
        utterance.onend = () => { 
            this.isSpeaking = false;
            this.currentUtterance = null;
        };
        utterance.onerror = () => { 
            this.isSpeaking = false;
            this.currentUtterance = null;
        };
        
        this.currentUtterance = utterance;
        this.synth.speak(utterance);
    }
    
    cleanText(text) {
        text = text.replace(/\s+/g, ' ').trim();
        if (text.length > 500) {
            text = text.substring(0, 500) + '...';
        }
        return text;
    }
    
    stop() {
        if (this.synth) {
            this.synth.cancel();
            this.isSpeaking = false;
            this.currentUtterance = null;
        }
    }
    
    getElementText(element) {
        if (element.hasAttribute('data-speak') && element.getAttribute('data-speak').trim()) {
            return element.getAttribute('data-speak').trim();
        }
        
        // Для ссылок и кнопок
        if (element.tagName === 'A' || element.tagName === 'BUTTON') {
            return element.innerText.trim();
        }
        
        if (element.tagName.match(/^H[1-6]$/)) {
            return element.innerText.trim();
        }
        
        if (element.classList && element.classList.contains('building-card')) {
            const title = element.querySelector('h2');
            const shortDesc = element.querySelector('p');
            let text = '';
            if (title) text += title.innerText + '. ';
            if (shortDesc) text += shortDesc.innerText.substring(0, 200);
            return text;
        }
        
        if (element.classList && element.classList.contains('filter-btn')) {
            return element.innerText.trim();
        }
        
        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            const label = document.querySelector(`label[for="${element.id}"]`);
            if (label) {
                return label.innerText.trim();
            }
            return element.placeholder || element.name || '';
        }
 
        let text = element.innerText || element.textContent;
        if (text && text.length > 300) {
            text = text.substring(0, 300) + '...';
        }
        return text ? text.trim() : '';
    }
    
    addHoverSpeak() {
        const elements = document.querySelectorAll(
            'a, button, h1, h2, h3, h4, p, span, div, ' +
            '.building-card, .info-item, .feature-box, .image-caption-box, ' +
            '.filter-btn, .read-more, .back-link, .suggest-btn, ' +
            '[data-speak], .main-nav a, .city-links a, ' +
            '.building-card h2, .building-card p, .filter-info, ' +
            '.meta-info, .audio-section, .image-section, .tactile-section, ' +
            '.sound-section, .accessibility-section, .description-section, ' +
            '.info-grid, .accessibility-btn'
        );
        
        console.log(`🔊 Найдено элементов для озвучки при наведении: ${elements.length}`);
        
        elements.forEach(element => {

            element.removeEventListener('mouseenter', this.handleMouseEnter);
            element.removeEventListener('mouseleave', this.handleMouseLeave);
            

            element.addEventListener('mouseenter', (e) => {
                this.stop();
                
                let text = this.getElementText(element);
                if (text && text.length > 0) {
                    console.log(`🖱️ Наведение: "${text.substring(0, 60)}..."`);
                    this.speak(text);
                }
                e.stopPropagation();
            });
        });
    }
    
    addFocusSpeak() {
        const focusElements = document.querySelectorAll(
            'a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])'
        );
        
        focusElements.forEach(element => {
            element.addEventListener('focus', (e) => {
                this.stop();
                let text = this.getElementText(element);
                if (text) {
                    console.log(`⌨️ Фокус (Tab): "${text.substring(0, 60)}..."`);
                    this.speak(text);
                }
                e.stopPropagation();
            });
        });
    }
    
    addSpeechControls() {
        const toolbar = document.querySelector('.accessibility-toolbar');
        if (toolbar) {
            if (!toolbar.querySelector('.stop-speech-btn')) {
                const stopBtn = document.createElement('button');
                stopBtn.textContent = '⏹️ Остановить озвучку';
                stopBtn.className = 'accessibility-btn stop-speech-btn';
                stopBtn.setAttribute('aria-label', 'Остановить текущую озвучку');
                stopBtn.onclick = () => {
                    this.stop();
                    console.log('⏹️ Озвучка остановлена пользователем');
                };
                toolbar.appendChild(stopBtn);
            }
        }
    }
}

class AccessibilityModes {
    constructor() {
        this.init();
    }
    
    init() {
        this.addModeButtons();
        this.loadSavedMode();
    }
    
    addModeButtons() {
        const toolbar = document.querySelector('.accessibility-toolbar');
        if (!toolbar) return;
        
        if (toolbar.querySelector('.mode-btn')) return;
        
        const highContrastBtn = document.createElement('button');
        highContrastBtn.textContent = '🌙 Высокий контраст (жёлтый/чёрный)';
        highContrastBtn.className = 'accessibility-btn mode-btn';
        highContrastBtn.onclick = () => this.toggleHighContrast();
        
        const largeTextBtn = document.createElement('button');
        largeTextBtn.textContent = '🔍 Крупный текст (+50%)';
        largeTextBtn.className = 'accessibility-btn mode-btn';
        largeTextBtn.onclick = () => this.toggleLargeText();
        
        const resetBtn = document.createElement('button');
        resetBtn.textContent = '🔄 Сбросить настройки';
        resetBtn.className = 'accessibility-btn mode-btn';
        resetBtn.onclick = () => this.resetModes();
        
        toolbar.appendChild(highContrastBtn);
        toolbar.appendChild(largeTextBtn);
        toolbar.appendChild(resetBtn);
    }
    
    toggleHighContrast() {
        document.body.classList.toggle('high-contrast-yellow');
        localStorage.setItem('highContrast', document.body.classList.contains('high-contrast-yellow'));
    }
    
    toggleLargeText() {
        document.body.classList.toggle('large-text');
        localStorage.setItem('largeText', document.body.classList.contains('large-text'));
    }
    
    resetModes() {
        document.body.classList.remove('high-contrast-yellow', 'large-text');
        localStorage.removeItem('highContrast');
        localStorage.removeItem('largeText');
    }
    
    loadSavedMode() {
        if (localStorage.getItem('highContrast') === 'true') {
            document.body.classList.add('high-contrast-yellow');
        }
        if (localStorage.getItem('largeText') === 'true') {
            document.body.classList.add('large-text');
        }
    }
}

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.tts = new TextToSpeech();
    window.accessibility = new AccessibilityModes();
});