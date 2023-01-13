---
title: "Przetwarzanie Cyfrowe Obrazów"
subtitle: "rozpoznawanie logo sieci sklepów Kaufland"
author: [Domański Piotr 293102]
date: "2022-01-13"
titlepage: true
header-includes:
   - \usepackage{multirow}
   - \usepackage{float}
   - \usepackage{graphicx}
   - \usepackage{subfigure}
...

# Zadanie realizowane w ramach projektu

W ramach projektu realizowana była implementacja procedur wstępnego przetwarzania, segmentacji, wyznaczania cech oraz identyfikacji obiektów na obrazach cyfrowych. Powstały w ramach projektu program powinien poprawnie rozpoznawać wybrane obiekty dla reprezentatywnego zestawu obrazów wejściowych. W trakcie projektu należało przetestować wybrane algorytmy i ocenić ich praktyczą przydatność.

# Rozpoznawany obiekt - logo Kaufland

Logo sieci sklepów Kaufland można znaleźć nie tylko w samym sklepie, ale również na produktach produkowanych w ramach ich marki: Kaufland Classic. Warto zaznaczyć, że logo umieszczane na szyldach sklepowych różni się od loga umieszczanego na produktach. Porównanie różnych wersji widoczne jest na rysunku \ref{loga}.

\begin{figure}[H]
\centering
\subfigure[]{\includegraphics[width=.4\textwidth]{media/logo2.png}}
\subfigure[]{\includegraphics[width=.2\textwidth]{media/logo1.png}}
\subfigure[]{\includegraphics[width=.15\textwidth]{media/logo3.png}}
\caption{Różne wersje loga Kaufland}
\label{loga}
\end{figure}

Ze względu na różne wersje loga Kaufland, konieczne jest rozpoznawanie jedynie ich części wspólnej przedstawionej na rysunku \ref{logo_wspolne}.

\begin{figure}[H]
\centering
\includegraphics[width=.2\textwidth]{media/logo_main.png}
\caption{Część wspólna różnych wersji logo Kaufland}
\label{logo_wspolne}
\end{figure}

Część wspólna różnych wersji logo Kaufland jest kształtu kwadratu i składa się z:

1. czerwonej ramki
2. dwóch czerwonych kwadratów wewnątrz ramki
3. dwóch czerwonych trójkątów wewnątrz ramki, będących wzajemnym odbiciem w pionie

Warto zaznaczyć, że powierzchnia pomiędzy wymienionymi elementami nie jest biała, a transparentna i na niektórych produktach marki ma inny kolor niż biały. Dodatkowo, wewnątrz ramki może znajdować się tekst "Kaufland". Ze względu na te rozbieżności, powierzchnia ta nie jest rozpoznawana w ramach projektu.

# Akwizycja obrazu

Logo Kaufland zostało przeze mnie wybrane jako obiekt rozpoznawany w ramach projektu, ponieważ właśnie w tej sieci sklepów najczęściej wykonuję zakupy, dzięki czemu wszystkie zdjęcia analizowanego zbioru danych zostały wykonane przeze mnie osobiście. Zbiór danych składa się z 6 zdjęć. Zdjęcia zostały wykonane w różnych warunkach oświetleniowych przy pomocy telefonu komórkowego, natomiast na żadnym z nich nie ma wyraźnych zakłóceń, są ogólnie dobrej jakości. Zbiór danych został przedstawiony na rysunku \ref{zbior}.

Pierwsze dwa zdjęcia zbioru danych przedstawiają logo Kaufland na szyldach sklepowych, pierwsze stanowi przypadek prosty natomiast drugie ma stanowić przypadek trudny do analizy, poniważ szyld znajduje się na szklanych drzwiach i jest zakłucony przez logo umieszczone po drugiej ich stronie.

Kolejne dwa zdjęcia przedstawiają logo znajdujące się na produktach marki Kaufland Classic z widocznymi produktami innych  marek i ich logami. Specjalnie umieszczono na nich produkty innych firm z czerwonymi logami.

Piąte zdjęcie przedstawia logo sklepu Kaufland na materiałowej reklamówce.

Ostatnie zdjęcie przedstawia dwa produkty Kaufland Classic obok siebie, co ma za zadanie zweryfikować możliwość rozpoznania wielu log na jednym zdjęciu.

\begin{figure}[H]
\centering
\subfigure[]{\includegraphics[width=.3\textwidth]{../data/kaufland1.png}}
\subfigure[]{\includegraphics[width=.25\textwidth]{../data/kaufland2.png}}
\subfigure[]{\includegraphics[width=.3\textwidth]{../data/kaufland3.png}}
\subfigure[]{\includegraphics[width=.3\textwidth]{../data/kaufland4.png}}
\subfigure[]{\includegraphics[width=.25\textwidth]{../data/kaufland5.png}}
\subfigure[]{\includegraphics[width=.3\textwidth]{../data/kaufland6.png}}
\caption{Zbiór testowy}
\label{zbior}
\end{figure}

# Algorytm wykrywania logo Kaufland

Algorytm do wykrywania logo Kaufland można podzielić na poniższe fazy:

1. wstępne przetwarzanie, zmiana rozmiaru i poprawa jakości obrazu
2. zmiana przestrzeni barw na HSV - rozdzielenie informacji o kolorze, nasyceniu i jasności
3. segmentacji - wydzielenie obszarów
4. wyznaczenie cech dla każdego obszaru
5. identyfikacja kształtów na podstawie ich opisów
6. rozpoznanie loga jako złożenie wielu kształtów

## Użyte narzędzia

Projekt zaimplementowano w języku programowania Python z wykorzystaniem pakietu OpenCV jedynie w ramach dozwolonych funkcji: wczytania i wyświetlenia obrazu oraz rysowania prostokąta do wyrysowania bounding box.

Ponieważ język Python jest wolniejszy od C++, implementowane algorytmy były silnie optymalizowane w celu maksymalizacji wykorzystania biblioteki do obliczeń numerycznych Numpy.

Dodatkowo, przy prezentacji wyników pośrednich t.j. segmentacji wykorzystano bibliotekę Matplotlib. Pozwala ona na interakcję z wyswietlanym obrazem, np. powiększaniem obszarów co znacznie ułatwiło analizę na etapie implementacji.

Wykorzystano najnowszą dostępną wersję języka Python - 3.11.

## Wstępne przetwarzanie

Wstępne przetwarzanie ma na celu poprawę sprawności działania algorytmu poprzez poprawę jakości obrazu oraz zmiejszenie jego rozmiarów.

### Zmiana rozmiaru

Pierwszym etapem wstępnego przetwarzania jest przeskalowanie obrazu do mniejszych rozmiarów w celu zmniejszenia złożoności obliczeniowej powiązanej z analizowaniem pojedynczych pikseli.

W tym celu zaimplementowano metodę interpolacji najbliższym sąsiadem. W programie domyślnie zdjęcia przetwarzane w wielkości dwa razy mniejszej niż oryginał.

\begin{figure}[H]
\centering
\subfigure[]{\includegraphics[width=.49\textwidth]{../data/kaufland3.png}}
\subfigure[]{\includegraphics[width=.49\textwidth]{media/nn.png}}
\caption{Obraz oryginalny vs. przeskalowany metodą interpolacji najbliższym sąsiadem}
\label{interpolacja}
\end{figure}

### Poprawa jakości

Do poprawy jakości zostały zaimplementowane:

1. filtr gaussa
2. filtr medianowy
3. wyrównywanie histogramu

Ponieważ jakoś zdjęć ze zbioru danych jest bardzo dobra, wykorzystanie tych metod jest opcjonalne. Wyrównywanie histogramu okazało się najbardziej pomocne przy zdjęciach wykonanych na terenie sklepu wykonanych przy silnym sztucznym świetle.

Filtry gaussa i medianowy są użyteczne przy przetwarzaniu w pełnej rozdzielczości, bez skalowania. Pozwalają one na dokładniejszą segmentację obiektów, co uniemożliwia delikatny szum np. dla zdjęcia 2. Natomiast zastosowanie ich przy skali 0.5 prowadzi do nie rozpoznania małych logo, ponieważ łączy ze sobą ich składowe elementy rozdzielone momentami jedynie jednym pikselem.

### Zmiana przestrzeni barw

W ramach projektu zaimplementowałem konwersję z przestrzeni barw BGR do HSV. Wynika to z charakteru segmentacji: interesują nas bowiem elementy o zadanym kolorze, dlatego możliwość prostej analizy koloru jest bardzo istotna. Ponieważ efekty nakładane są na oryginalny obraz, konwersja odwrotna nie była implementowana.

Przestrzeń HSV reprezentowana jest w programie w zakresie 0-255 dla każdej składowej, dzięki czemu możliwy jest prosty zapis do pliku obrazu w formacie HSV i jego prezentacja.


\begin{figure}[H]
\centering
\subfigure[]{\includegraphics[width=.49\textwidth]{../data/kaufland3.png}}
\subfigure[]{\includegraphics[width=.49\textwidth]{media/hsv.png}}
\caption{Porównanie tego samego zdjęcia w przestrzeni barw BGR i HSV}
\label{hsv}
\end{figure}

Działanie algorytmu zostało porównane z konwersją przy użyciu biblioteki OpenCV dając wyniki z zakresu błędu przybliżenia wartości zmiennoprzecinkowych do wartości stałych.

### Segmentacja

Poprawna segmentacja obrazu jest podstawą wykrywania logo. W programie została użyta segmentacja przez progowanie wartości H, S i V.

Ponieważ kolor czerwony leży w przestrzeni barw w okolicach wartości granicznej składowej H (wartości z zakresu 0-20 oraz 170-255 przy 256 stopniowej skali Hue), wykorzystano dwie rozdzielne maski dla wartości H z zakresu 0-20 i 170-255 oraz je połączono. Warto zaznaczyć, że ta maska jest delikatnie rozszerzona o wartości z zakresu różu i pomarańczowego, co było wymagane dla paru przypadków z danych testowych - na obrazku pierwszym obwódka loga kafuland jest delikatnie różowa, a na piątym ciemne elementy są postrzegane jako ciemny brązowy.

Przy segmentacji wykorzystano również składowe nasycenia i jasności. Poniższa tabela prezentuje wartości progowe obu masek, a rysunek \ref{mask} porównanie obrazu wsadowego do otrzymanej maski.

| maska     | H min | H max | S min | S max | V min | V max |
|-----------|-------|-------|-------|-------|-------|-------|
| czerowny1 | 0     | 20    | 145   | 255   | 40    | 255   |
| czerwony2 | 170   | 255   | 145   | 255   | 40    | 255   |


\begin{figure}[H]
\centering
\subfigure[]{\includegraphics[width=.49\textwidth]{../data/kaufland3.png}}
\subfigure[]{\includegraphics[width=.49\textwidth]{media/mask.png}}
\caption{Porównanie zdjęcia i otrzymanej maski binarnej dla koloru czerwonego}
\label{mask}
\end{figure}

Następnie zastosowano zmodyfikowany algorytm flood fill do rozdzielenia fragmentów maski na segmenty, wykorzystywany do wypełniania zamkniętych obszarów. Algorytm ten dla kolejnych białych pikseli maski binarnej metodą przeszukiwania wszerz koloruje na losowy, unikalny dla maski kolor wszystkie sąsiadujące z nim piksele.

Kolejnym etapem segmentacji jest usunięcie zbyt małych i zbyt dużych obszarów. Tutaj usunięto obszary bardzo małe (poniżej 0.01% obszaru całego zdjęcia) oraz bardzo duże (powyżej 9% wielkosći zdjęcia, nawet jak logo zajmuje cały obszar zdjęcia żaden jego element nie będzie miał tak dużej powierzchni).

Wynik podziału na segmenty przedstawiony został na rysunku \ref{segmenty}.


\begin{figure}[H]
\centering
\subfigure[]{\includegraphics[width=.49\textwidth]{../data/kaufland3.png}}
\subfigure[]{\includegraphics[width=.49\textwidth]{media/segments.png}}
\caption{Porównanie zdjęcia i otrzymanych segmentów}
\label{segmenty}
\end{figure}

### Wyznaczanie cech

W celu wyznaczenia cech segmentów skorzystano z momentów centralnych oraz współczynnika Blaira-Blissa. Momenty geometryczne centralne oraz współczynnik Blaira-Blissa cechują się niezmiennosćią niezależnie od dokonanej translacji co jest szczególnie istotne ze względu na dwa rózne trójkąty w logo Kaufland, gdzie jeden jest odbiciem drugiego w pionie, oraz pod kątem wykrywania logo Kaufland niezależnie od jego orientacji.

Dla każdego momentu obliczane są wartości niezmienniczych momentów M1-M6 oraz W4 (współczynnik Blaira-Blissa).

### Indentyfikacja kształtów

Na zbiorze danych wyznaczono wartości graniczne dla wyznaczonych cech pozwalające na identyfikację: trójkątów, kwardatów oraz ramki. Wartości te przedstawiono w tabeli \ref{cechy}. Na rysunku \ref{trojkaty_i_kwardaty} przedstawiono wyniki identyfikacji zadanych kształtów.

\begin{table}[]
\begin{tabular}{|ll|l|l|l|l|l|l|l|l|}
\hline
\multicolumn{2}{|l|}{kształt}                        & M1 & M2 & M3 & M4 & M5 & M6 & M7 & W4 \\ \hline
\multicolumn{1}{|l|}{\multirow{2}{*}{trójkąt}} & min & 0.2 & 0.0072 & 0.0028 & 0.0001 & -384.0 & -0.000285 & 0.0078 & 0.83\\ \cline{2-10} 
\multicolumn{1}{|l|}{}                         & max & 0.231 & 0.016 & 0.0063 & 0.00031 & 660.432 & 1.68798e-05 & 0.0096 & 0.885\\ \hline
\multicolumn{1}{|l|}{\multirow{2}{*}{kwadrat}} & min & 0.164 & 2.149e-05 & 0.0 & 0.0 & -0.05 & -4.513e-07 & 0.0066 & 0.9643 \\ \cline{2-10} 
\multicolumn{1}{|l|}{}                         & max & 0.17115 & 0.001381 & 4.042e-05 & 8.95e-07 & 0.002 & 6.242e-07 & 0.007 & 0.985 \\ \hline
\multicolumn{1}{|l|}{\multirow{2}{*}{ramka}}   & min & 1.38 & 0.00045 & -0.0167 & -0.0075 & -201e9 & -46230.5029 & 0.47 & 0.26 \\ \cline{2-10} 
\multicolumn{1}{|l|}{}                         & max & 2.304 & 0.1105 & 0.0182 & 0.01536 & 272345e9 & 25.18 & 1.33 & 0.34 \\ \hline
\end{tabular}
\caption{wyznaczone zakresy cech dla poszczególnych kształtów}
\label{cechy}
\end{table}

\begin{figure}[H]
\centering
\subfigure[]{\includegraphics[width=.49\textwidth]{../data/kaufland3.png}}
\subfigure[]{\includegraphics[width=.49\textwidth]{media/shapes.png}}
\caption{Porównanie zdjęcia i zidentyfikowanych kształtów. Kolorem czerwonym oznaczono ramkę, zielonym kwadraty a niebieskim trójkąty}
\label{trojkaty_i_kwardaty}
\end{figure}

### Rozpoznanie logo

Po identyfikacji kształtów, ostatnim elementem jest rozpoznanie logo. W tym celu wystarczy znaleźć ramkę, wewnątrz której są dokładnie 2 kwardaty i 2 trójkąty. Efekt końcowy można zapisać w postaci oryginalnego zdjęcia z naniesionym bounding boxem lub maski binarnej. Na rysunkach \ref{wyniki1}, \ref{wyniki2} i \ref{wyniki3} przedstawiono wszystkie zdjęcia ze zbioru danych oraz wyniki dla nich otrzymane.


\begin{figure}[H]
\centering
\subfigure[]{\includegraphics[width=.49\textwidth]{../output/kaufland1.png}}
\subfigure[]{\includegraphics[width=.49\textwidth]{../output/kaufland1_mask.png}}
\subfigure[]{\includegraphics[width=.49\textwidth]{../output/kaufland2.png}}
\subfigure[]{\includegraphics[width=.49\textwidth]{../output/kaufland2_mask.png}}
\subfigure[]{\includegraphics[width=.49\textwidth]{../output/kaufland3.png}}
\subfigure[]{\includegraphics[width=.49\textwidth]{../output/kaufland3_mask.png}}
\caption{Porównanie zdjęć ze zbioru danych oraz otrzymanych dla nich wyników}
\label{wyniki1}
\end{figure}


\begin{figure}[H]
\centering
\subfigure[]{\includegraphics[width=.49\textwidth]{../output/kaufland4.png}}
\subfigure[]{\includegraphics[width=.49\textwidth]{../output/kaufland4_mask.png}}
\subfigure[]{\includegraphics[width=.49\textwidth]{../output/kaufland5.png}}
\subfigure[]{\includegraphics[width=.49\textwidth]{../output/kaufland5_mask.png}}
\caption{Porównanie zdjęć ze zbioru danych oraz otrzymanych dla nich wyników, ciąg dalszy}
\label{wyniki2}
\end{figure}

\begin{figure}[H]
\centering
\subfigure[]{\includegraphics[width=.49\textwidth]{../output/kaufland6.png}}
\subfigure[]{\includegraphics[width=.49\textwidth]{../output/kaufland6_mask.png}}
\caption{Porównanie zdjęć ze zbioru danych oraz otrzymanych dla nich wyników, ciąg dalszy}
\label{wyniki3}
\end{figure}

# Efekt i wnioski

Program zaimplementowany w ramach projektu pozwala na dowolne sterowanie użytymy algorytmami, np. użycie zadanych metod poprawy jakości, sterowanie skalą w jakiej zdjęcie jest przetwarzanie, minimalną i maksymalną wielkością segmentów, pozwala na wyświetlanie efektów na każdym kroku i wybór efektu końcowego (maska czy boungding box). Udało się poprawnie rozpoznać loga dla każdego zdjęcia ze zbioru danych.

Możliwym usprawnieniem byłoby rozpoznawanie dodatkowo napisów - "Kaufland" wewnątrz ramki lub po jej prawej stronie oraz "Classic" pod ramką. Sprowadzałoby się to do wyznaczenia cech dla każdej litery oraz modyfikacji rozpoznawania loga tak, aby pod uwagę brany był również napis.
