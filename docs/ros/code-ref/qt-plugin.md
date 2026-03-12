# Qt Plugin (C++)

C++ Qt GUI 플러그인 프로젝트


[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/cpp_qt_plugin/){ .md-button }

#### `cpp_qt_plugin/src/main.cpp`

```cpp
// pip install pybind11
#include "./mainwindow.cpp"
#include <QApplication>
#include <pybind11/embed.h>
#include <memory>
#include <rclcpp/rclcpp.hpp>

namespace py = pybind11;

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    QApplication app(argc, argv);

    auto qt_node = rclcpp::Node::make_shared("qt_visualizer_node");

    MainWindow mainWindow(qt_node);
    mainWindow.show();

    auto executor = std::make_shared<rclcpp::executors::SingleThreadedExecutor>();
    executor->add_node(qt_node);

    std::thread rosThread([&]() { executor->spin(); });

    int ret = app.exec();

    rclcpp::shutdown();
    rosThread.join();

    return ret;
}

```

#### `cpp_qt_plugin/src/mainwindow.cpp`

```cpp
#include "./qt_gui.h"
#include <QApplication>
#include <QClipboard>
#include <QString>
#include <QPainter>
#include <QTimer>
#undef slots                // Qt과 매크로 slots 비활성화
#include <pybind11/embed.h>
#define slots Q_SLOTS       // Qt의 slots 매크로를 다시 정의
#include <algorithm>
#include <iostream>
#include <mutex>
#include <string>
#include <thread>
#include <vector>
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/float64_multi_array.hpp>

namespace py = pybind11;
py::scoped_interpreter guard{};

using namespace std;

#define ACC 60
#define VEL 60
#define ON 1
#define OFF 0


class PlotWidget : public QWidget {

public:
    explicit PlotWidget(QWidget* parent = nullptr)
        : QWidget(parent), timeStep(0) {
        data.fill(0.0);
    }

    void addDataPoint(const std::array<double, 6>& newData) {
        data = newData;
        timeStep++;
        update();
    }

protected:
    void paintEvent(QPaintEvent* event) override {
        Q_UNUSED(event);
        QPainter painter(this);
        painter.setRenderHint(QPainter::Antialiasing);

        painter.fillRect(this->rect(), Qt::white);
# ... (438 more lines)
```

#### `cpp_qt_plugin/src/qt_gui.h`

```cpp
/********************************************************************************
** Form generated from reading UI file 'qt_gui.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef QT_GUI_H
#define QT_GUI_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLCDNumber>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QSlider>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QHBoxLayout *horizontalLayout;
    QVBoxLayout *verticalLayout;
    QGridLayout *labelGrid;
    QLabel *cartesianPositionLabel;
    QLabel *jointPositionLabel;
    QGridLayout *jointCartesianControlGrid;
    QLabel *jointLabelHeader;
    QLabel *statusLabelHeader;
    QLabel *valueLabelHeader;
    QLabel *jointLabel1;
    QLineEdit *jointstatus1;
    QLineEdit *jointvalue1;
    QPushButton *incrementJoint1;
    QPushButton *decrementJoint1;
    QLabel *jointLabel2;
    QLineEdit *jointstatus2;
    QLineEdit *jointvalue2;
    QPushButton *incrementJoint2;
    QPushButton *decrementJoint2;
    QLabel *jointLabel3;
    QLineEdit *jointstatus3;
# ... (789 more lines)
```

#### `cpp_qt_plugin/resource/qt_gui.h`

```cpp
/********************************************************************************
** Form generated from reading UI file 'qt_gui.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef QT_GUI_H
#define QT_GUI_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLCDNumber>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QSlider>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QHBoxLayout *horizontalLayout;
    QVBoxLayout *verticalLayout;
    QGridLayout *labelGrid;
    QLabel *cartesianPositionLabel;
    QLabel *jointPositionLabel;
    QGridLayout *jointCartesianControlGrid;
    QLabel *jointLabelHeader;
    QLabel *statusLabelHeader;
    QLabel *valueLabelHeader;
    QLabel *jointLabel1;
    QLineEdit *jointstatus1;
    QLineEdit *jointvalue1;
    QPushButton *incrementJoint1;
    QPushButton *decrementJoint1;
    QLabel *jointLabel2;
    QLineEdit *jointstatus2;
    QLineEdit *jointvalue2;
    QPushButton *incrementJoint2;
    QPushButton *decrementJoint2;
    QLabel *jointLabel3;
    QLineEdit *jointstatus3;
# ... (789 more lines)
```

#### `cpp_qt_plugin/package.xml`

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>cpp_qt_plugin</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="imt025@naver.com">rokey</maintainer>
  <license>TODO: License declaration</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <depend>rclcpp</depend>
  <depend>std_msgs</depend>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>
  <buildtool_depend>qtbase5-dev</buildtool_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>

```
