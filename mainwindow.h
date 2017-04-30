#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QNetworkReply>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    void replyFinished(QNetworkReply* reply);
    void getCoordinates(void);
    void getImage(double, double, double, double, QString added, QString arrayfires);
    void drawImage(QString);
    ~MainWindow();

private slots:



private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
