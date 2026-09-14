const PRACTICALS = [
  ['01','Image Operations','Pixel-level transformations',['Grayscale','Negative','Threshold','Bitwise AND','Bitwise OR','Bitwise XOR','Addition','Subtraction']],
  ['02','Geometric Transformation','Change image geometry',['Resize','Rotate','Translate','Flip','Affine','Perspective']],
  ['03','Spatial Enhancement','Improve contrast and detail',['Histogram Equalization','CLAHE','Gamma Correction','Log Transform','Unsharp Mask']],
  ['04','Spatial Filters','Smooth and detect local detail',['Mean','Gaussian','Median','Bilateral','Laplacian','Sobel','Prewitt']],
  ['05','Image Inpainting','Repair selected damaged areas',['Telea','Navier-Stokes']],
  ['06','Lossless Compression','Encode and reconstruct without data loss',['RLE','Huffman']],
  ['07','Morphological Operations','Shape-based image processing',['Erosion','Dilation','Opening','Closing','Gradient','Top-hat','Black-hat']],
  ['08','Correlation Detection','Find a template inside an image',['Template Matching']],
  ['09','Colour Spaces','Explore common colour models',['RGB','Grayscale','HSV','LAB','YCrCb']],
  ['10','Edge Detection','Highlight object boundaries',['Canny','Sobel','Prewitt','Roberts','Laplacian']]
];

const OP = {
  'Grayscale':'grayscale','Negative':'negative','Threshold':'threshold','Bitwise AND':'bitwise_and','Bitwise OR':'bitwise_or','Bitwise XOR':'bitwise_xor','Addition':'add','Subtraction':'subtract',
  'Resize':'resize','Rotate':'rotate','Translate':'translate','Flip':'flip','Affine':'affine','Perspective':'perspective',
  'Histogram Equalization':'hist_eq','CLAHE':'clahe','Gamma Correction':'gamma','Log Transform':'log','Unsharp Mask':'unsharp',
  'Telea':'telea','Navier-Stokes':'ns','RLE':'rle','Huffman':'huffman',
  'Erosion':'erosion','Dilation':'dilation','Opening':'opening','Closing':'closing','Gradient':'gradient','Top-hat':'tophat','Black-hat':'blackhat',
  'Template Matching':'template','RGB':'rgb','HSV':'hsv','LAB':'lab','YCrCb':'ycrcb',
  'Mean':'mean','Gaussian':'gaussian','Median':'median','Bilateral':'bilateral','Laplacian':'laplacian','Sobel':'sobel','Prewitt':'prewitt',
  'Canny':'canny','Roberts':'roberts'
};

let practical = null;
let operation = null;
const $ = id => document.getElementById(id);
const cards = $('practicals');

PRACTICALS.forEach((item, index) => {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'practical';
  button.innerHTML = `<span class="p-number">${item[0]}</span><span class="p-content"><b>${item[1]}</b><small>${item[2]}</small></span><span class="p-arrow">→</span>`;
  button.addEventListener('click', () => selectPractical(index));
  cards.appendChild(button);
});

$('image').addEventListener('change', handleImage);
const drop = $('drop');
['dragenter','dragover'].forEach(type => drop.addEventListener(type, event => { event.preventDefault(); drop.classList.add('drag'); }));
['dragleave','drop'].forEach(type => drop.addEventListener(type, event => { event.preventDefault(); drop.classList.remove('drag'); }));
drop.addEventListener('drop', event => {
  const file = event.dataTransfer.files[0];
  if (!file) return;
  const dt = new DataTransfer(); dt.items.add(file); $('image').files = dt.files; handleImage();
});

function handleImage() {
  const file = $('image').files[0];
  $('fileName').textContent = file ? file.name : 'Choose an image';
  if (!file) return;
  $('inputPreview').classList.remove('hidden');
  $('inputInfo').textContent = `${file.name} · ${(file.size / 1024 / 1024).toFixed(2)} MB`;
  const reader = new FileReader();
  reader.onload = e => $('inputThumb').src = e.target.result;
  reader.readAsDataURL(file);
  updateRunState();
}

function selectPractical(index) {
  practical = PRACTICALS[index];
  document.querySelectorAll('.practical').forEach((card, i) => card.classList.toggle('active', i === index));
  $('opTitle').textContent = practical[1];
  $('controlsBox').innerHTML = `<div class="field"><label>Operation</label><select id="op">${practical[3].map(name => `<option>${name}</option>`).join('')}</select></div><div id="params"></div>`;
  $('op').addEventListener('change', buildControls);
  buildControls();
  document.querySelector('.controls').scrollIntoView({behavior:'smooth', block:'center'});
}

function rangeField(label, id, value, min, max, step='1') {
  return `<div class="field"><label>${label}<span id="${id}v">${value}</span></label><input id="${id}" type="range" value="${value}" min="${min}" max="${max}" step="${step}"></div>`;
}

function buildControls() {
  operation = OP[$('op').value];
  let html = '';
  const secondNeeded = ['bitwise_and','bitwise_or','bitwise_xor','add','subtract','template','telea','ns'].includes(operation);
  if (secondNeeded) {
    const template = operation === 'template';
    const mask = operation === 'telea' || operation === 'ns';
    html += `<div class="second-box"><div class="second-title">${template ? 'Template image' : mask ? 'Mask image' : 'Second image'} <b>${template || mask ? 'Required' : 'Required'}</b></div><input type="file" id="second" accept="image/png,image/jpeg,image/bmp,image/webp"><small>${template ? 'Upload the smaller object/image you want to locate inside the main image.' : mask ? 'White areas of this mask mark the damaged region to repair.' : 'Upload the second source image. It will be resized to the main image dimensions.'}</small></div>`;
  }
  if (operation === 'threshold') html += rangeField('Threshold','threshold',128,0,255);
  if (operation === 'resize') html += rangeField('Scale','scale',1,0.1,4,0.1);
  if (operation === 'rotate') html += rangeField('Angle','angle',0,-180,180);
  if (operation === 'translate') { html += rangeField('X','x',30,-300,300); html += rangeField('Y','y',30,-300,300); }
  if (operation === 'flip') html += `<div class="field"><label>Direction</label><select id="mode"><option value="horizontal">Horizontal</option><option value="vertical">Vertical</option><option value="both">Both</option></select></div>`;
  if (operation === 'clahe') html += rangeField('Clip limit','clip',2,1,8,0.5);
  if (operation === 'gamma') html += rangeField('Gamma','gamma',1,0.1,5,0.1);
  if (operation === 'unsharp') { html += rangeField('Kernel','kernel',5,3,15,2); html += rangeField('Amount','amount',1.5,0.1,3,0.1); }
  if (['mean','gaussian','median','bilateral','erosion','dilation','opening','closing','gradient','tophat','blackhat'].includes(operation)) html += rangeField('Kernel size','kernel',5,3,15,2);
  if (['erosion','dilation','opening','closing','gradient','tophat','blackhat'].includes(operation)) { html += rangeField('Threshold','threshold',128,0,255); html += rangeField('Iterations','iterations',1,1,5); }
  if (operation === 'canny') { html += rangeField('Low threshold','low',80,0,255); html += rangeField('High threshold','high',160,1,255); }
  if (operation === 'telea' || operation === 'ns') html += rangeField('Inpaint radius','radius',3,1,10,1);
  if (operation === 'perspective') html += rangeField('Perspective','perspective',0.12,0,0.30,0.01);
  if (operation === 'affine') { html += rangeField('X offset','dx',40,0,150); html += rangeField('Y offset','dy',30,0,150); }
  $('params').innerHTML = html;
  document.querySelectorAll('#params input[type="range"]').forEach(input => input.addEventListener('input', () => $(input.id+'v').textContent = input.value));
  if ($('second')) $('second').addEventListener('change', updateRunState);
  updateRunState();
}

function updateRunState() {
  const hasImage = !!$('image').files[0];
  const needsSecond = ['template','telea','ns','bitwise_and','bitwise_or','bitwise_xor','add','subtract'].includes(operation);
  const hasSecond = !!$('second')?.files[0];
  $('run').disabled = !(hasImage && operation && (!needsSecond || hasSecond));
}

$('run').addEventListener('click', async () => {
  const file = $('image').files[0];
  if (!file) return;
  const form = new FormData();
  form.append('image', file);
  form.append('operation', operation);
  document.querySelectorAll('#params input, #params select').forEach(element => {
    if (element.type === 'file') { if (element.files[0]) form.append('second', element.files[0]); }
    else form.append(element.id, element.value);
  });

  $('run').disabled = true;
  $('message').className = 'message processing';
  $('message').textContent = 'Processing image…';
  try {
    const response = await fetch('/process', {method:'POST', body:form});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Processing failed.');
    $('result').src = data.url + '?t=' + Date.now();
    $('placeholder').style.display = 'none';
    $('download').href = data.download;
    $('download').hidden = false;
    $('message').className = 'message ok';
    $('message').textContent = data.title;
    renderStats(data.extra || {});
    $('insights').classList.remove('hidden');
    $('inputSize').textContent = data.input_size;
    $('outputSize').textContent = data.output_size;
    $('operationName').textContent = data.title;
    drawHistogram(data.histogram, data.output_histogram);
  } catch (error) {
    $('message').className = 'message error';
    $('message').textContent = error.message;
  } finally {
    updateRunState();
  }
});

function renderStats(extra) {
  const entries = Object.entries(extra);
  $('stats').innerHTML = entries.length ? entries.map(([key,value]) => `<div class="stat"><span>${key.replaceAll('_',' ')}</span><b>${value}</b></div>`).join('') : '';
}

function drawHistogram(input, output) {
  const canvas = $('histCanvas');
  const ctx = canvas.getContext('2d');
  const ratio = window.devicePixelRatio || 1;
  const width = canvas.clientWidth || 900;
  const height = 190;
  canvas.width = width * ratio; canvas.height = height * ratio; ctx.setTransform(ratio,0,0,ratio,0,0);
  ctx.clearRect(0,0,width,height);
  const pad = 18, base = height - 18;
  ctx.strokeStyle = 'rgba(86, 76, 63, .16)';
  for (let i=0;i<4;i++) { const y=pad+i*(base-pad)/3; ctx.beginPath(); ctx.moveTo(pad,y); ctx.lineTo(width-pad,y); ctx.stroke(); }
  function line(arr, color) {
    ctx.beginPath(); arr.forEach((value,i)=>{ const x=pad+i*(width-2*pad)/(arr.length-1); const y=base-value*(base-pad); i?ctx.lineTo(x,y):ctx.moveTo(x,y); }); ctx.strokeStyle=color; ctx.lineWidth=2; ctx.stroke();
  }
  line(input, '#9b6b3d');
  line(output, '#536b55');
}
