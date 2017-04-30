#include "mainwindow.h"
#include <QApplication>
#include <QtNetwork>
#include <QNetworkAccessManager>
#include <QBuffer>
#include <QByteArray>
#include <QIODevice>
#include <QSplashScreen>
#include <QPixmap>
#include <QtDebug>



int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.getCoordinates();
    w.show();

    return a.exec();
}






