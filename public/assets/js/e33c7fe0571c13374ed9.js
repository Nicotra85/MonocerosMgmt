
document.querySelectorAll('img.article-cover').forEach(img=>{if(img.parentElement.classList.contains('motion-frame'))return;const frame=document.createElement('div');frame.className='motion-frame';img.before(frame);frame.append(img);});
