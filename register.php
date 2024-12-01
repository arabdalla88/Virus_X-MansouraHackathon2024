<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "user_authentication";

$conn = new mysqli($servername, $username, $password, $dbname);


if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $email = $_POST["email"];
    $password = $_POST["password"];

    $confirmPassword = isset($_POST["confirmPassword"]) ? $_POST["confirmPassword"] : null;

    // التحقق من تطابق كلمة المرور
    if ($password !== $confirmPassword) {
        echo "كلمة المرور وتأكيد كلمة المرور غير متطابقين.";
    } else {
        // التحقق مما إذا كان اسم المستخدم أو البريد الإلكتروني مستخدمًا بالفعل
        $checkUserQuery = "SELECT * FROM users WHERE username='$username' OR email='$email'";
        $result = $conn->query($checkUserQuery);


        if ($result->num_rows > 0) {
            echo "اسم المستخدم أو البريد الإلكتروني مستخدم بالفعل. الرجاء اختيار اسم أو بريد آخر.";
        } else {
            // إذا لم يتم العثور على اسم المستخدم أو البريد الإلكتروني، قم بإضافة الحساب
            $insertQuery = "INSERT INTO users (username, email, password) VALUES ('$username', '$email', '$password')";

            if ($conn->query($insertQuery) === TRUE) {
                echo "تم إنشاء الحساب بنجاح!";
                header("Location: index.html?$username");
                exit;
            } else {
                echo "فشل إنشاء الحساب: " . $conn->error;
            }
        }
    }
}

$conn->close();

?>


<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: grid;
            height: 100vh;
            align-items: center;
            justify-content: center;
            align-content: space-evenly;
        }

        h2 {
            text-align: center;
        }

        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
            text-align: center;
        }

        form {
            display: flex;
            flex-direction: column;
        }

        label {
            margin-bottom: 8px;
        }

        input {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            box-sizing: border-box;
        }

        button {
            background-color: blue;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        a {
            text-decoration: none;
            color: blue;
        }

        a:hover {
            text-decoration: underline;
        }
    </style>



    <title>Sign Up</title>
</head>

<body>
    <h2>Sign Up</h2>
    <form action="register.php" method="post">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>

        <label for="confirmPassword">Confirm Password:</label>
        <input type="password" id="confirmPassword" name="confirmPassword" required>

        <button type="submit">Sign Up</button>
    </form>
    <p>Already have an account? <a href="login_process.php">Log In</a></p>
</body>

</html>