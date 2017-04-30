#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QApplication>
#include <QtNetwork>
#include <QNetworkAccessManager>
#include <QBuffer>
#include <QByteArray>
#include <QIODevice>
#include <QSplashScreen>
#include <QPixmap>
#include <QJsonValue>
#include <QJsonDocument>
#include <QJsonObject>
#include <QVariantMap>
#include <QJsonArray>
#include <QtDebug>


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

}

MainWindow::~MainWindow()
{
    delete ui;
}



void MainWindow::getCoordinates(void)
{
   QNetworkRequest request(QUrl("http://ec2-54-93-96-33.eu-central-1.compute.amazonaws.com:5000/51.763635/8.065624/51.754994/8.045626"));
   request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
   QJsonObject json;
   QNetworkAccessManager* nam =  new QNetworkAccessManager;
   QNetworkReply *reply = nam->get(request);
   while(!reply->isFinished())
        qApp->processEvents();
   QByteArray response_data = reply->readAll();
   QJsonDocument jsonn = QJsonDocument::fromJson(response_data);
   reply->deleteLater();
   QJsonObject a = jsonn.object();
   QJsonValue v = a.value(QString("fires"));
   QJsonValue va = a.value(QString("path"));
   QJsonArray array = v.toArray();
   QJsonArray arr = va.toArray().at(0).toArray();
   QJsonArray seba = va.toArray();
   double m1 = arr.at(0).toDouble();
   double m2 = arr.at(1).toDouble();
   QJsonObject item = array.at(0).toObject();
   QJsonValue val2 = item.value("coords");
   QJsonArray arraypoint = val2.toArray();
   double lat = arraypoint.at(0).toDouble();
   double lng = arraypoint.at(1).toDouble();
   QString arrayfires;
   foreach (const QJsonValue & value, array)
    {
        double dd1 = value.toObject().value("coords").toArray().at(0).toDouble();
        double dd2 = value.toObject().value("coords").toArray().at(1).toDouble();
        arrayfires.append("&x[]=").append(QString::number(dd1)).append("&y[]=").append(QString::number(dd2));
    }

   QNetworkRequest request2(QUrl("http://ec2-54-93-96-33.eu-central-1.compute.amazonaws.com:5000/users"));
   request2.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
   QJsonObject json2;
   QNetworkAccessManager* nam2 =  new QNetworkAccessManager;
   QNetworkReply *reply2 = nam2->get(request2);
   while(!reply2->isFinished())
        qApp->processEvents();
   QByteArray response_data2 = reply2->readAll();
   jsonn = QJsonDocument::fromJson(response_data2);
   reply->deleteLater();
   a = jsonn.object();
   v = a.value(QString("users"));
   array = v.toArray();
   QString add;
   foreach (const QJsonValue & value, array)
    {
        double d1 = value.toArray().at(0).toDouble();
        double d2 = value.toArray().at(1).toDouble();
        add.append("%26markers=").append(QString::number(d1)).append(",").append(QString::number(d2));
    }

   getImage(lat,lng, m1, m2, add, arrayfires);
   ui->labely->setText(QString::number(m1));
   ui->labelx->setText(QString::number(m2));

}



void MainWindow::getImage(double lat, double lng, double m1, double m2, QString added, QString arrayfires)
{
   QString url = "http://172.16.176.204/index.php?lat=";
   url.append(QString::number(lat));
   url.append("&lng=");
   url.append(QString::number(lng));
   url.append("&mark1=");
   url.append(QString::number(m1));
   url.append("&mark2=");
   url.append(QString::number(m2));
   url.append("&mark3=");
   url.append(added);
   url.append(arrayfires);
   qDebug() << url;
   QUrl url2(url);
   QNetworkRequest request(url2);
   QNetworkAccessManager* nam =  new QNetworkAccessManager;
   QNetworkReply *reply = nam->get(request);
   while(!reply->isFinished())
        qApp->processEvents();
   QString response_data = reply->readAll();
   QString rp;
   for (int i = 0; i < response_data.length() - 1; i++)
       rp[i] = response_data[i];
   drawImage(rp);
}


void MainWindow::drawImage(QString url)
{
    QNetworkAccessManager* netAccManager = new QNetworkAccessManager;
         QNetworkRequest request(url);
         QNetworkReply *reply = netAccManager->get(request);
         QEventLoop loop;
         QObject::connect(reply,SIGNAL(finished()),&loop,SLOT(quit()));
         loop.exec();
         QByteArray bytes = reply->readAll();
         QImage img(20, 20, QImage::Format_Indexed8);
         img.loadFromData(bytes);
         QImage img2 = img.scaled(640, 480, Qt::KeepAspectRatio);
         ui->label->setPixmap(QPixmap::fromImage(img2));
}




