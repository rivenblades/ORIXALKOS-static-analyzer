#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTextEdit>
#include "highlighter.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
public slots:
//    void newFile();
//    void openFile(const QString &path = QString());

private:
    Ui::MainWindow *ui;

    void setupEditor();
    void setupFileMenu();

    QTextEdit *editor;
    Highlighter *highliter;
};

#endif // MAINWINDOW_H
