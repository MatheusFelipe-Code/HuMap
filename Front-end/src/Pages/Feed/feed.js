/* ==========================
   PEGAR CSRF
========================== */
function getCSRFToken() {
	return document.cookie
		.split('; ')
		.find((row) => row.startsWith('csrftoken='))
		?.split('=')[1];
}

/* ==========================
   FEED
========================== */
document.addEventListener('DOMContentLoaded', () => {
	document.querySelectorAll('.post-feed').forEach((post) => {
		const id = post.dataset.id;

		// ===== LIKE =====
		const likeBtn = post.querySelector('.like-btn-feed');
		const likeCount = post.querySelector('.like-count-feed');
		let liked = likeBtn.classList.contains('fa-solid');
		let likes = parseInt(likeCount.textContent);

		likeBtn.addEventListener('click', () => {
			likeBtn.classList.add('like-animate-feed');
			setTimeout(() => likeBtn.classList.remove('like-animate-feed'), 300);

			liked = !liked;
			likes = liked ? likes + 1 : likes - 1;
			likeBtn.classList.toggle('fa-solid', liked);
			likeBtn.classList.toggle('fa-regular', !liked);

			// 🔧 ALTERAÇÃO 1 (AQUI)
			likeBtn.style.color = liked ? 'red' : '';

			likeCount.textContent = likes;

			const formData = new URLSearchParams();
			formData.append('curtir_denuncia_id', id);

			fetch('/feed/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
					'X-CSRFToken': getCSRFToken(),
				},
				body: formData.toString(),
			});
		});

		// ===== COMENTÁRIOS =====
		const commentInput = post.querySelector('.comment-input-feed');
		const sendBtn = post.querySelector('.send-comment-feed');
		const commentList = post.querySelector('.comment-list-feed');
		const commentCount = post.querySelector('.comment-count-feed');

		sendBtn.addEventListener('click', (e) => {
			e.stopPropagation();
			e.preventDefault();

			const text = commentInput.value.trim();
			if (!text) return;

			const formData = new URLSearchParams();
			formData.append('curtir_denuncia_id', id);
			formData.append('comentario_texto', text);

			fetch('/feed/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
					'X-CSRFToken': getCSRFToken(),
				},
				body: formData.toString(),
			})
				.then((res) => {
					if (!res.ok) throw new Error('Erro ao enviar comentário');
					return res.text();
				})
				.then(() => {
					const div = document.createElement('div');
					div.className = 'comment-item-feed';
					div.textContent = `${requestUserName}: ${text}`;
					commentList.appendChild(div);

					commentInput.value = '';
					commentCount.textContent = parseInt(commentCount.textContent) + 1;
				})
				.catch((err) => console.error(err));
		});

		// ===== CARREGAR COMENTÁRIOS EXISTENTES =====
		const comentariosExistentes = post.dataset.comentarios
			? JSON.parse(post.dataset.comentarios)
			: [];

		comentariosExistentes.forEach((c) => {
			const div = document.createElement('div');
			div.className = 'comment-item-feed';
			div.textContent = `${c.usuario}: ${c.texto}`;
			commentList.appendChild(div);
		});
		commentCount.textContent = comentariosExistentes.length;

		// ===== FAVORITAR =====
		const favBtn = post.querySelector('.fav-btn-feed');
		favBtn.addEventListener('click', () => {
			const ativo = favBtn.classList.toggle('ativo');

			// 🔧 ALTERAÇÃO 2 (AQUI)
			favBtn.style.color = ativo ? 'gold' : '';
		});

		// ===== COPIAR LINK =====
		const linkBtn = post.querySelector('.link-btn-feed');
		linkBtn.addEventListener('click', () => {
			const url = `${window.location.origin}/denuncia/${id}/`;
			navigator.clipboard.writeText(url);
			alert('Link copiado!');
		});

		// ===== REPORTAR =====
		const reportBtn = post.querySelector('.report-btn-feed');
		reportBtn.addEventListener('click', () => {
			document.querySelector('.modal-overlay-feed').classList.add('active');
		});
	});
});

/* ==========================
   MODAL DE REPORTAR
========================== */
const modal = document.querySelector('.modal-overlay-feed');
if (modal) {
	modal.querySelector('.cancel-feed').addEventListener('click', () => {
		modal.classList.remove('active');
	});

	modal.querySelector('.ok-feed').addEventListener('click', () => {
		const textarea = modal.querySelector('.modal-textarea-feed');
		if (!textarea.value.trim()) return;
		alert('Problema enviado:\n\n' + textarea.value);
		modal.classList.remove('active');
	});
}
