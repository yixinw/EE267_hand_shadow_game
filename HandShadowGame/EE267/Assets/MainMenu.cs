using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MainMenu : MonoBehaviour {
	private int counter = 0;
	private Texture2D tex_1 = null;
	private Texture2D tex_2 = null;
	private Texture2D tex_3 = null;
	private bool game_start = false;

	void Start() {
		tex_1 = new Texture2D (2, 2);
		tex_2 = new Texture2D (2, 2);
		tex_3 = new Texture2D (2, 2);

		// Load texture from disk.
		byte[]  fileData;
		string filePath_1 = "Assets/Handpainted Forest Environment Free Sample/Textures/number-solid-1.jpg";
		if (System.IO.File.Exists (filePath_1)) {
			fileData = System.IO.File.ReadAllBytes (filePath_1);
			tex_1 = new Texture2D (2, 2);
			tex_1.LoadImage (fileData);
		}
		string filePath_2 = "Assets/Handpainted Forest Environment Free Sample/Textures/number-solid-2.jpg";
		if (System.IO.File.Exists (filePath_2)) {
			fileData = System.IO.File.ReadAllBytes (filePath_2);
			tex_2 = new Texture2D (2, 2);
			tex_2.LoadImage (fileData);
		}
		string filePath_3 = "Assets/Handpainted Forest Environment Free Sample/Textures/number-solid-3.jpg";
		if (System.IO.File.Exists (filePath_3)) {
			fileData = System.IO.File.ReadAllBytes (filePath_3);
			tex_3 = new Texture2D (2, 2);
			tex_3.LoadImage (fileData);
		}
	}

	void Update() {
		// There are two ways to start the game
		// One is to hit space. The other is to 
		// wait for the counter to be accumulated to 150

		if (Input.GetKeyDown ("space")) {
			game_start = true;
		}
		if (counter < 300)
			counter += 1;
		if (game_start) {
			counter = 145;
			game_start = false;
		}

		// Load counting down textures
		if (counter == 150) {
			GetComponent<Renderer> ().material.SetTexture ("_MainTex", tex_3);
		}
		if (counter == 200) {
			GetComponent<Renderer> ().material.SetTexture ("_MainTex", tex_2);
		}
		if (counter == 250) {
			GetComponent<Renderer> ().material.SetTexture ("_MainTex", tex_1);
		}
		if (counter == 300) {
			SceneManager.LoadScene (1);
		}
	}
}
	