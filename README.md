# RussianArticles-PronominalAnaphora

Каждая строка корпуса соответствует одному анафорическому соотношению “антецедент - местоименная анафора” и их морфологическим признакам. 
Для антецедента:
- часть речи
- одушевленность
- род
- число
- категория падежа


Для анафора:
- часть речи
- категория лица
- категория падежа
- число



Для извлечения данных признаков использовался pymorphy2 - морфологический анализатор для русского языка, написанный на языке Python и использующий словари из OpenCorpora. [Korobov M. Morphological analyzer and generator for Russian and Ukrainian languages //International Conference on Analysis of Images, Social Networks and Texts. – Springer, Cham, 2015. – С. 320-332.]
