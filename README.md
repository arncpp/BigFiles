<h1 id="earley-algorithm">Задача 233. Передача файлов</h1>
</blockquote>
<h1 id="-arncpp">Гайд по запуску проекта</h1>
<h2 id="-pycharm">Как запустить проект через консоль</h2>
<details>
<summary><strong>Первый этап: установка python и flask.
<h5 id="-python3-pygame-"><em>Если у вас уже установлен python 3.10 и вы можете самостоятельно установить библиотеку flask — пропустите этот этап</em></h5></summary>
<p><strong>1. Скачайте python3 с официального <a href="https://www.python.org/downloads/">сайта</a> и установите его.</strong>
<strong>2. Во время установки <em>обязательно</em> поставьте галочку &quot;Add Python 3.x to PATH&quot;.</strong>
<img src="https://python-scripts.com/wp-content/uploads/2018/06/win-install-dialog.40e3ded144b0.png" alt="add path screenshot"></p>
<p><strong>3. Когда установка закончится запустите консоль нажать комбинацию Win + R.

</details>

<details><summary>Второй этап: скачивание и запуск проекта.</summary>
<p><strong>1. Скачайте проект с github любым удобным для вас способом.</strong></p>
<p><strong>2. В консоли перейдите в папку. 
<p><strong>3. Запустите проект.
<p><strong>Команды, необходимые для запуска через консоль:
<p><code>git clone https://github.com/arncpp/KIS_task.git</code></p>
<p><code>pip install flask</code></p>
<p><code>pip install requests</code></p>
<p><code>cd</code></p>
<p><code>python client.py</code></p>
<p>Поднять тестовый сервер на <code>localhost</code> можно так:</p>
<p><code>FLASK_APP=server.py flask </code></p>

</details>

</details>
</details>




<h2 id="-">Что это?</h2>
<p>У пользователей часто возникает потребность передать большие файлы. Важно, чтобы это не занимало больших ресурсов времени, а также при передаче файлы не повредились. К счастью, у нас есть высокие технологии, чтобы решить эту проблему. </p>
<p>При запуске программы пользователь вводит название файла, который хочет передать и количество потоков. </p>
<h2 id="-">Как это работает?</h2>
<p>Сервер реализован с помощью микро-фреймворка <code>Flask</code>. Мы возлагаем на него всего две задачи:</p>
<ol>
<li>Не забывать, от кого он получает файл.</li>
<li>Сохранять переданный файл и проверять его на целостность.</li>
</ol>
<p>Первая проблема в решается довольно просто: мы храним IP-адреса пользователей и соответствующую им сессию <code>UploadSession</code>. Также у нас имеется все данные о пользователях, которые когда-либо передавали свои файлы. Как только пользователь передал файл, мы удаляем его сессию. 
<p>Для того чтобы решить вторую проблему, в клиенте мы разделяем файл на части и передаем побайтово потокам и серверу. Сервер в свою очередь сохраняет все эти файлы во временной папке <code>temp</code>, а после того как все части файла загружены, соеденяет их в один и удаляет временную папку. </p>
<p>Пользователь же может себе поменять адрес сервара (<code>main_url</code> в <code>urls.py</code>).
<p>Пример работы:</p>
<pre><code><span class="hljs-keyword">Input</span>:
file_name test.jpg
<span class="hljs-keyword">count_threads 5</span>
transfer_file
<span class="hljs-keyword">exit</span>
Output:
Your file has been uploaded successfully!

