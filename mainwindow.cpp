#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    //setupFileMenu();
    setupEditor();

    setCentralWidget(editor);
    setWindowTitle("ORIXALKOS -IDE-");
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::setupEditor(){
    QFont font;
    font.setFamily("Courier");
    font.setFixedPitch(true);
    font.setPointSize(10);

    editor = new QTextEdit;
    editor->setFont(font);

    highliter = new Highlighter(editor->document());

    QFile file("mainwindow.h");
    if(file.open(QFile::ReadOnly|QFile::Text)){
        editor->setPlainText(file.readAll());
    }
    editor->setStyleSheet("background-color:#888;");

//    editor->setTextBackgroundColor(Qt::darkGray);
}
