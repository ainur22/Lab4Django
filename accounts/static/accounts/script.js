(function () {
  const btnMenu = document.getElementById("btnMenu");
  const drawer = document.getElementById("drawer");
  const backdrop = document.getElementById("backdrop");
  const btnClose = document.getElementById("btnCloseDrawer");

  function openDrawer() {
    if (!drawer) return;
    drawer.classList.add("open");
    if (backdrop) backdrop.hidden = false;
  }

  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove("open");
    if (backdrop) backdrop.hidden = true;
  }

  if (btnMenu) btnMenu.addEventListener("click", openDrawer);
  if (btnClose) btnClose.addEventListener("click", closeDrawer);
  if (backdrop) backdrop.addEventListener("click", closeDrawer);

  const aiFloatBtn = document.getElementById("aiFloatBtn");
  const aiPop = document.getElementById("aiPop");
  const aiPopClose = document.getElementById("aiPopClose");

  function closeAiPop() {
    if (!aiPop) return;
    aiPop.classList.remove("show");
  }

  function toggleAiPop(e) {
    if (e) e.stopPropagation();
    if (!aiPop) return;
    aiPop.classList.toggle("show");
  }

  if (aiFloatBtn && aiPop) {
    aiFloatBtn.addEventListener("click", toggleAiPop);
  }

  if (aiPopClose && aiPop) {
    aiPopClose.addEventListener("click", closeAiPop);
  }

  document.addEventListener("click", (e) => {
    if (!aiPop || !aiFloatBtn) return;

    const clickedInsidePop = aiPop.contains(e.target);
    const clickedFloatBtn = aiFloatBtn.contains(e.target);

    if (!clickedInsidePop && !clickedFloatBtn) {
      closeAiPop();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeDrawer();
      closeAiPop();
    }
  });

  const accordionBtns = document.querySelectorAll(".accordion-btn");

  accordionBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const item = btn.closest(".accordion-item");
      if (!item) return;
      item.classList.toggle("open");
    });
  });

  const levelRange = document.getElementById("levelRange");
  const levelOut = document.getElementById("levelOut");

  if (levelRange && levelOut) {
    levelOut.textContent = levelRange.value;

    levelRange.addEventListener("input", () => {
      levelOut.textContent = levelRange.value;
    });
  }

  const homeFaqButtons = document.querySelectorAll(".home-faq-q");

  homeFaqButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const item = btn.closest(".home-faq-item");
      if (!item) return;
      item.classList.toggle("open");
    });
  });
})();

(function () {
  const carousel = document.getElementById("guideCarousel");
  if (!carousel) return;

  const slides = carousel.querySelectorAll(".guide-slide");
  const dots = carousel.querySelectorAll(".guide-dots button");
  const prev = document.getElementById("guidePrev");
  const next = document.getElementById("guideNext");

  if (!slides.length) return;

  let current = 0;
  let autoSlide;

  function showSlide(index) {
    slides.forEach((slide, i) => {
      slide.classList.toggle("active", i === index);
    });

    dots.forEach((dot, i) => {
      dot.classList.toggle("active", i === index);
    });

    current = index;
  }

  function nextSlide() {
    const newIndex = (current + 1) % slides.length;
    showSlide(newIndex);
  }

  function prevSlide() {
    const newIndex = (current - 1 + slides.length) % slides.length;
    showSlide(newIndex);
  }

  function startAuto() {
    stopAuto();
    autoSlide = setInterval(nextSlide, 4500);
  }

  function stopAuto() {
    if (autoSlide) clearInterval(autoSlide);
  }

  if (next) {
    next.addEventListener("click", () => {
      nextSlide();
      startAuto();
    });
  }

  if (prev) {
    prev.addEventListener("click", () => {
      prevSlide();
      startAuto();
    });
  }

  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      showSlide(index);
      startAuto();
    });
  });

  carousel.addEventListener("mouseenter", stopAuto);
  carousel.addEventListener("mouseleave", startAuto);

  showSlide(0);
  startAuto();
})();

(function () {
  const chatForm = document.getElementById("chatForm");
  const chatInput = document.getElementById("chatInput");
  const chatWindow = document.getElementById("chatWindow");
  const voiceBtn = document.getElementById("voiceBtn");
  const assistantStatus = document.getElementById("assistantStatus");
  const voiceHint = document.getElementById("voiceHint");
  const toggleVoiceReadBtn = document.getElementById("toggleVoiceReadBtn");
  const quickPills = document.querySelectorAll(".ai-quick-pill");

  if (!chatForm || !chatInput || !chatWindow) return;

  let recognition = null;
  let isRecognizing = false;

  let mediaRecorder = null;
  let audioChunks = [];
  let mediaStream = null;
  let isRecording = false;

  let autoSpeakEnabled = true;

  function getCookie(name) {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
    return "";
  }

  function scrollChatBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  function speakText(text) {
    if (!("speechSynthesis" in window) || !text) return;

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "kk-KZ";
    utterance.rate = 1;
    utterance.pitch = 1;
    window.speechSynthesis.speak(utterance);
  }

  function appendBotMessage(text) {
    const div = document.createElement("div");
    div.className = "ai-msg ai-msg-bot";
    div.innerHTML = `
      <div class="ai-msg-avatar">AI</div>
      <div class="ai-msg-body">
        <div class="ai-bubble ai-bubble-bot"></div>
        <div class="ai-msg-meta">
          EduMentor AI
          <button type="button" class="speak-btn" aria-label="Оқу">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M5 9v6h4l5 4V5L9 9H5Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
              <path d="M17 9.5C18.2 10.4 19 11.9 19 13.5C19 15.1 18.2 16.6 17 17.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
      </div>
    `;

    div.querySelector(".ai-bubble").textContent = text;
    div.querySelector(".speak-btn").setAttribute("data-speak", text);
    chatWindow.appendChild(div);
    scrollChatBottom();

    if (autoSpeakEnabled) {
      speakText(text);
    }
  }

  function appendUserMessage(text) {
    const div = document.createElement("div");
    div.className = "ai-msg ai-msg-user";
    div.innerHTML = `
      <div class="ai-msg-body">
        <div class="ai-bubble ai-bubble-user"></div>
        <div class="ai-msg-meta">Сіз</div>
      </div>
    `;
    div.querySelector(".ai-bubble").textContent = text;
    chatWindow.appendChild(div);
    scrollChatBottom();
  }

  function appendTypingRow() {
    removeTypingRow();

    const div = document.createElement("div");
    div.className = "ai-msg ai-msg-bot";
    div.id = "typingRow";
    div.innerHTML = `
      <div class="ai-msg-avatar">AI</div>
      <div class="ai-msg-body">
        <div class="ai-bubble ai-bubble-bot ai-typing">
          <span></span><span></span><span></span>
        </div>
        <div class="ai-msg-meta">EduMentor AI жазып жатыр...</div>
      </div>
    `;
    chatWindow.appendChild(div);
    scrollChatBottom();
  }

  function removeTypingRow() {
    const typingRow = document.getElementById("typingRow");
    if (typingRow) typingRow.remove();
  }

  function setVoiceState({ listening = false, status = "", hint = "" }) {
    if (voiceBtn) {
      voiceBtn.classList.toggle("is-listening", listening);
    }
    if (status && assistantStatus) assistantStatus.textContent = status;
    if (hint && voiceHint) voiceHint.textContent = hint;
  }

  function getDemoReply(text) {
    const t = text.toLowerCase();

    if (t.includes("тарих")) {
      return "Қазақстан тарихы бойынша оқу жоспарын кезең-кезеңімен құрған дұрыс: ежелгі кезең, орта ғасырлар, кеңестік дәуір және тәуелсіз Қазақстан.";
    }

    if (t.includes("матем")) {
      return "Математикада алдымен әлсіз тақырыптарды анықтап, формулаларды қайталап, күн сайын есеп шығару практикасын жасау керек.";
    }

    if (t.includes("биология")) {
      return "Биологияда терминдерді жаттау ғана емес, тақырыптар арасындағы байланысты түсіну де маңызды.";
    }

    if (t.includes("физика")) {
      return "Физика үшін теория, формула және есеп шығару қатар жүруі керек. Қай бөлім қиын екенін жазсаң, нақтылап көмектесемін.";
    }

    if (t.includes("жоспар")) {
      return "Жақсы, мен саған күндерге бөлінген нақты оқу жоспарын жасап бере аламын. Қай пән екенін де жаза кет.";
    }

    return "Жақсы, түсіндім. Осы тақырыпты саған қарапайым тілмен түсіндіріп, керек болса оқу жоспарын да жасап бере аламын.";
  }

  function sendMessage(text) {
    const cleanText = text.trim();
    if (!cleanText) return;

    appendUserMessage(cleanText);
    chatInput.value = "";
    chatInput.focus();

    appendTypingRow();

    setVoiceState({
      listening: false,
      status: "Жауап дайындап жатыр...",
      hint: "Күте тұр"
    });

    setTimeout(() => {
      removeTypingRow();
      const reply = getDemoReply(cleanText);
      appendBotMessage(reply);

      setVoiceState({
        listening: false,
        status: "Онлайн • жауап беруге дайын",
        hint: "Enter — жіберу"
      });
    }, 900);
  }

  function detectSpeechRecognition() {
    return window.SpeechRecognition || window.webkitSpeechRecognition || null;
  }

  function initSpeechRecognition() {
    const SR = detectSpeechRecognition();
    if (!SR) return false;

    recognition = new SR();
    recognition.lang = "kk-KZ";
    recognition.interimResults = true;
    recognition.continuous = false;

    let finalTranscript = "";

    recognition.onstart = () => {
      isRecognizing = true;
      finalTranscript = "";
      setVoiceState({
        listening: true,
        status: "Тыңдап тұр...",
        hint: "Сөйлей бер"
      });
    };

    recognition.onresult = (event) => {
      let interimText = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;

        if (event.results[i].isFinal) {
          finalTranscript += transcript + " ";
        } else {
          interimText += transcript;
        }
      }

      chatInput.value = (finalTranscript + interimText).trim();
    };

    recognition.onerror = (event) => {
      isRecognizing = false;
      setVoiceState({
        listening: false,
        status: "Voice қатесі: " + event.error,
        hint: "Қайта байқап көр"
      });
    };

    recognition.onend = () => {
      isRecognizing = false;
      setVoiceState({
        listening: false,
        status: "Дауыстық мәтін дайын",
        hint: "Enter — жіберу"
      });
      chatInput.focus();
    };

    return true;
  }

  async function startBrowserRecognition() {
    if (!recognition) {
      const ok = initSpeechRecognition();
      if (!ok) return false;
    }

    if (isRecognizing) {
      recognition.stop();
      return true;
    }

    recognition.start();
    return true;
  }

  async function startRecorderFallback() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      appendBotMessage("Бұл браузерде микрофон API қолжетімсіз.");
      return;
    }

    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunks = [];
      mediaRecorder = new MediaRecorder(mediaStream, { mimeType: "audio/webm" });

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        try {
          setVoiceState({
            listening: false,
            status: "Аудио жіберіліп жатыр...",
            hint: "Күте тұр"
          });

          const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
          const formData = new FormData();
          formData.append("audio", audioBlob, "voice.webm");

          const transcribeUrl =
            window.transcribeAudioUrl ||
            (typeof transcribeAudioUrl !== "undefined" ? transcribeAudioUrl : null);

          if (!transcribeUrl) {
            throw new Error("transcribe_audio URL табылмады");
          }

          const response = await fetch(transcribeUrl, {
            method: "POST",
            headers: {
              "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData
          });

          const data = await response.json();

          if (!response.ok || !data.ok) {
            throw new Error(data.error || "Transcription failed");
          }

          chatInput.value = data.text || "";
          if (assistantStatus) assistantStatus.textContent = "Дауыстық мәтін дайын";
          if (voiceHint) voiceHint.textContent = "Enter — жіберу";
          chatInput.focus();

        } catch (error) {
          if (assistantStatus) assistantStatus.textContent = "Қате шықты";
          if (voiceHint) voiceHint.textContent = "Қайта байқап көр";
          appendBotMessage("Voice transcription қатесі: " + error.message);
        } finally {
          if (mediaStream) {
            mediaStream.getTracks().forEach((track) => track.stop());
            mediaStream = null;
          }
          isRecording = false;
          if (voiceBtn) voiceBtn.classList.remove("is-listening");
        }
      };

      mediaRecorder.start();
      isRecording = true;

      setVoiceState({
        listening: true,
        status: "Жазып жатыр...",
        hint: "Тоқтату үшін қайта бас"
      });

    } catch (error) {
      appendBotMessage("Микрофонға рұқсат берілмеді немесе құрылғы табылмады.");
      setVoiceState({
        listening: false,
        status: "Микрофон қолжетімсіз",
        hint: "Рұқсат беріп қайта байқап көр"
      });
    }
  }

  function stopRecorderFallback() {
    if (mediaRecorder && isRecording) {
      mediaRecorder.stop();
    }
  }

  async function handleVoiceClick() {
    const hasSpeechRecognition = !!detectSpeechRecognition();

    if (hasSpeechRecognition) {
      await startBrowserRecognition();
      return;
    }

    if (isRecording) {
      stopRecorderFallback();
    } else {
      await startRecorderFallback();
    }
  }

  chatForm.addEventListener("submit", function (e) {
    e.preventDefault();
    sendMessage(chatInput.value);
  });

  chatInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage(chatInput.value);
    }
  });

  if (voiceBtn) {
    voiceBtn.addEventListener("click", handleVoiceClick);
  }

  if (toggleVoiceReadBtn) {
    toggleVoiceReadBtn.addEventListener("click", function () {
      autoSpeakEnabled = !autoSpeakEnabled;
      this.classList.toggle("is-off", !autoSpeakEnabled);

      if (!autoSpeakEnabled && "speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
    });
  }

  quickPills.forEach((btn) => {
    btn.addEventListener("click", function () {
      chatInput.value = this.dataset.text || "";
      chatInput.focus();
    });
  });

  document.addEventListener("click", function (e) {
    const speakBtn = e.target.closest(".speak-btn");
    if (!speakBtn) return;

    const text = speakBtn.dataset.speak || "";
    if (text) speakText(text);
  });

  window.addEventListener("load", () => {
    scrollChatBottom();
    initSpeechRecognition();
  });
})();