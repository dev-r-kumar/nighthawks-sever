function showTab(tabId) {
  const tabs = document.querySelectorAll('.tab-content');
  tabs.forEach(tab => tab.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
}

async function createLicense() {
  const note = document.getElementById('note').value;
  const level = document.getElementById('level').value;
  const duration = document.getElementById('duration').value;
  const res = await fetch(`/createlicensekey?note=${note}&level=${level}&duration=${duration}`);
  const text = await res.text();
  document.getElementById('createResult').innerText = text;
}

async function register() {
  const key = document.getElementById('regKey').value;
  const user = document.getElementById('regUser').value;
  const pass = document.getElementById('regPass').value;
  const res = await fetch(`/register?key=${key}&user=${user}&password=${pass}`);
  const text = await res.text();
  document.getElementById('registerResult').innerText = text;
}

async function login() {
  const user = document.getElementById('loginUser').value;
  const pass = document.getElementById('loginPass').value;
  const res = await fetch(`/login?user=${user}&password=${pass}`);
  const text = await res.text();
  document.getElementById('loginResult').innerText = text;
}

async function checkDuration() {
  const user = document.getElementById('durUser').value;
  const pass = document.getElementById('durPass').value;
  const res = await fetch(`/accountduration?user=${user}&password=${pass}`);
  const text = await res.text();
  document.getElementById('durationResult').innerText = text;
}

async function patchPattern() {
  const pattern = document.getElementById('pattern').value;
  const res = await fetch(`/patchpattern?pattern=${encodeURIComponent(pattern)}`);
  const text = await res.text();
  document.getElementById('patchResult').innerText = text;
}

async function patchHead() {
  const offset = document.getElementById('offsetHead').value;
  const res = await fetch(`/patchheadoffset?offset=${encodeURIComponent(offset)}`);
  const text = await res.text();
  document.getElementById('patchResult').innerText = text;
}

async function patchLeftEar() {
  const offset = document.getElementById('offsetLeftEar').value;
  const res = await fetch(`/patchleftearoffset?offset=${encodeURIComponent(offset)}`);
  const text = await res.text();
  document.getElementById('patchResult').innerText = text;
}

async function patchRightEar() {
  const offset = document.getElementById('offsetRightEar').value;
  const res = await fetch(`/patchrightearoffset?offset=${encodeURIComponent(offset)}`);
  const text = await res.text();
  document.getElementById('patchResult').innerText = text;
}

async function patchLeftShoulder() {
  const offset = document.getElementById('offsetLeftShoulder').value;
  const res = await fetch(`/patchleftshoulderoffset?offset=${encodeURIComponent(offset)}`);
  const text = await res.text();
  document.getElementById('patchResult').innerText = text;
}

async function patchRightShoulder() {
  const offset = document.getElementById('offsetRightShoulder').value;
  const res = await fetch(`/patchrightshoulderoffset?offset=${encodeURIComponent(offset)}`);
  const text = await res.text();
  document.getElementById('patchResult').innerText = text;
}


async function patchStatus() {
  const status = document.getElementById("server-status").value;
  const res = await fetch(`/patchpanelstatus?status=${encodeURIComponent(status)}`);
  const text = await res.text();
  document.getElementById('patchResult').innerText = text;
}