# demo-alice-translate-skill
![Mole image](https://avatars.mds.yandex.net/get-dialogs/1017510/0479fa286034b99b6294/catalogue-icon-x3)

## Что это такое

В этом репозитории - пример простого навыка Алисы 
["Крот-полиглот"](https://dialogs.yandex.ru/store/skills/622af903-krot-poliglot)
, реализованного на Python с использованием 
[новых фич](https://yandex.ru/blog/dialogs/vesennee-obnovlenie-platformy-dialogov) 
[Яндекс.Диалогов](https://dialogs.yandex.ru/) -  [грамматик](https://yandex.ru/dev/dialogs/alice/doc/nlu-docpage/) и 
[хранилища состояний](https://yandex.ru/dev/dialogs/alice/doc/session-persistence-docpage/). 
Подробнее про эти фичи можно посмотреть в 
[видеоразборе обновлений платформы](https://www.youtube.com/watch?v=VLza91oQZDA&feature=youtu.be).

Навык занимается переводом слов и фраз между несколькими языковыми парами, 
используя API Яндекс.Переводчика, и немножко может поддерживать контекст диалога:

![Dialogue Image](image/dialogue.png)

Навык предназначен для публикации на 
[Yandex Cloud Functions](https://cloud.yandex.ru/docs/functions/) 
(для навыков Алисы это бесплатно, но нужно привязать карту). 
Впервые он был представлен на "Хакатоне 0 марта" 
([объявление](https://events.yandex.ru/events/hakaton-navykov-29-02-2020), 
[результаты](https://yandex.ru/blog/dialogs/kak-proshel-fevralskiy-khakaton)).

## Как запустить навык самостоятельно
1. Зарегистрироваться в [API Яндекс.Переводчика](https://yandex.ru/dev/translate/)
и получить токен доступа. Вставить его в переменную API_KEY в файле `translation.py`.
2. Зарегистрироваться в [Яндекс.Облаке](https://console.cloud.yandex.ru/) 
и, следуя [инструкции](https://cloud.yandex.ru/docs/functions/quickstart/function-quickstart), 
создать функцию на Python3.7
3. В редакторе кода этой функции создать файлы `main.py` и `translation.py`, 
и скопипастить в них содержимое соответстующих файлов из данного репозитория.
4. В поле "точка входа" в редакторе функции ввести `main.handler` - это имя
файла и питонячьей функции, которая собственно будет отвечать на запрос. 
5. В [консоли разработчика навыков](https://dialogs.yandex.ru/developer/)
создать новый навык, выбрав в качестве бэкенда "Функция в Яндекс.Облаке" и 
указав созданную вами функцию. 
Нужно также поставить галочку "использовать хранилище данных в навыке".
6. На подвкладке "Интенты" нужно накликать 5 новых интентов. 
В каждом из них нужно ввести название и id, равные имени файла (без расширения)
из папки grammars, а в поле грамматика скопипастить содержимое этого файла. 
Например, в интент с названием и ID `exit` нужно скопипастить содержимое файла
`grammars/exit.grammar`.
7. Всё готово! Вы можете протестировать навык во вкладке "тестирование". 
Если вас всё устраивает, можно отправить навык на модерацию и опубликовать его.
