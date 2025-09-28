# Autoweathertraffic
İstanbul için gerçek zamanlı hava durumu bilgisi veren aynı zamanda hava durumu üzerine uyarıda bulunan ve Kadıköy-Beşiktaş rotası için trafik yoğunluğunu ifade eden Python uygulaması.
Araç ekranında güncellenerek yer alan hava durumuna göre hem yazılı hem sesli uyarılar almak sürüş kalitesini arttırabilir.İstanbul'da trafik günlük hayatı büyük ölçüde etkiler.Trafik yoğunluğuna etki eden büyük bir faktör ise hava durumudur. Projede örnek olarak seçilen "Kadıköy-Beşiktaş" rotası üzerinden kullanıcı hem hava durumunu hem de trafik yoğunluğunun bilgisini alır.
Uygulama, Tkinter GUI arayüzü sayesinde kullanıcı dostu bir görselleştirme sağlar ve pyttsx3 kütüphanesi kullanılarak sesli uyarılar yapılır. Projede iki temel API kullanılmıştır: OpenWeatherMap API ile İstanbul için sıcaklık, nem ve hava durumu bilgisi alınır. TomTom Route Flow API ile Kadıköy-Beşiktaş rotasındaki trafik yoğunluğu, rota segmentleri bazında hesaplanarak yüzde değer olarak kullanıcıya sunulur. Bu teknolojilerin seçilme nedeni: OpenWeatherMap,Türkiye ve İstanbul için gerçek zamanlı hava durumu verisi sağlar. Sıcaklık, nem, yağış, kar ve sis gibi hava koşullarını hızlı ve güvenilir şekilde çekmek mümkündür.TomTom Route Flow API, Kadıköy-Beşiktaş gibi rotalarda trafik yoğunluğunu gerçek zamanlı ve detaylı olarak almayı sağlar. Diğer trafik API’lerine göre kullanımı daha kolay ve garantilidir; rota segmentleri bazında veri sunması, trafik yüzdesi hesaplamayı mümkün kılar. 
Kullanıcı arayüzü, hava durumu ve trafik yoğunluğunu her 10 dakikada bir güncelleyerek güncel bilgi sağlamaktadır. Öneri fonksiyonu, hava ve trafik durumuna göre sürüş uyarıları üretir: yağmurda yolun kaygan olduğu bilgisi ve hız azaltma, karda lastik kontrol uyarısı , sis durumunda farları yakma gibi tavsiyeler sesli (pyttsx3) ve yazılı olarak iletilir. 
Bu proje, Python ile API entegrasyonu, gerçek zamanlı veri işleme, GUI geliştirme ve sesli uyarı sistemleri konularında deneyim kazanmak isteyenler için ideal bir örnektir. Kullanılan kütüphaneler: requests (API çağrıları için), pyttsx3 (sesli uyarı), tkinter (GUI) ve Python 3.x standart kütüphaneleridir. 
Kurulum ve Çalıştırma: 1-Repository’yi klonlayın:
bash
git clone https://github.com/kullaniciAdi/IstanbulWeatherTrafficAssistant.git
cd IstanbulWeatherTrafficAssistant
2-Gerekli kütüphaneleri yükleyin 
pip install -r requirements.txt
3-main.py içindeki API key’leri kendi OpenWeatherMap ve TomTom key’lerinizle değiştirin.
4-Uygulamayı çalıştırın:
python main.py
Örnek Çıktı:
Hava (İstanbul): Rain
Sıcaklık: 18°C
Nem: 82%
Kadıköy → Beşiktaş Trafik Yoğunluğu: %75
Öneri: Yağmur yağıyor, yol kaygan. Lütfen hızını azalt ve farlarını aç. İstanbul trafiği yoğun, dikkatli sür!
