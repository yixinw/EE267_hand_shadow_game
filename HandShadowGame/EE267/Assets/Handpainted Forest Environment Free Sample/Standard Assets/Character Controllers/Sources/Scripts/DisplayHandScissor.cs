using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

using System;
using System.IO;
using System.Net.Sockets;
using System.Text;

public class DisplayHandScissor : MonoBehaviour {

	private GameObject congrats;
	private bool succeed = false;

	public Text scoreboard;
	public Text tutorial;
	private float rChannel = 0.0f;
	private int counter = 0;
	private int counter_text = 0;
	private int current_score = -1;
	private string score = "";
	s_TCP s_tcp = new s_TCP();

	// instructions in the tutorial scene
	private string tutorial_1 = "Put hand on right panel\n";
	private string tutorial_2 = "Great! Mimic the shadow\n";
	private string tutorial_3 = "So close!\n";
	private string tutorial_4 = "Congrats! U did it!\n";

	// Use this for initialization
	void Start () {
		// GetComponent<Renderer>().material.color = new Color(rChannel, 0.0f, 0.0f);
		s_tcp.setupSocket ();
		scoreboard.text = "Score N/A";
		tutorial.text = "This is a tutorial\n";
		congrats = GameObject.Find ("Congrats");
		congrats.SetActive (false);
	}

	// Update is called once per frame
	void Update () {

		counter += 1;
		if (counter > 5) {
			// add 0 after Hello, World! to tell server which shadow to load
			s_tcp.writeSocket ("Hello, World!0");
			byte[] buffer = s_tcp.readSocket ();
			if (buffer != null && buffer.Length > 0) {
				Debug.Log ("Received:" + Encoding.ASCII.GetString (buffer, 0, 5));
				// Create a texture. Texture size does not matter, since
				// LoadImage will replace with with incoming image size.
				if (buffer.Length < 10) {
					Debug.Log ("Succeed");
					current_score = 100;
				} else {
					Texture2D tex = new Texture2D (2, 2);
					byte[] score_buf = new byte[2];
					byte[] img_buf = new byte[buffer.Length - 2];
					Buffer.BlockCopy(buffer, 0, score_buf, 0, 2);
					Buffer.BlockCopy(buffer, 2, img_buf, 0, img_buf.Length);
					tex.LoadImage (img_buf);
					GetComponent<Renderer> ().material.SetTexture ("_MainTex", tex);
					score = System.Text.Encoding.UTF8.GetString (score_buf);
					scoreboard.text = "Score " + score;
					current_score = Int32.Parse(score);
					// tex.LoadImage (buffer);
					// GetComponent<Renderer> ().material.SetTexture ("_MainTex", tex);
				}
			} else {
				//Debug.Log ("Received nothing.");
			}
			counter = 0;
		}

		counter_text += 1;
		if (counter_text == 100) {
			tutorial.text = tutorial_1;
		} else if (counter_text > 100 && counter_text % 50 == 0) {
			// use counter_text and current_score to
			// decide which instruction to show
			if (succeed == true) {
				SceneManager.LoadScene (2);
			}
			if (current_score < 20) {
				tutorial.text = tutorial_1;
			} else if (current_score >= 20 && current_score <= 80) {
				tutorial.text = tutorial_2;
			} else if (current_score > 80 && current_score < 100) {
				tutorial.text = tutorial_3;
			} else {
				tutorial.text = tutorial_4;
				congrats.SetActive (true);
				succeed = true;
			}
		}

		// hit space to move to the next scene
		if (Input.GetKeyDown ("space")) {
			SceneManager.LoadScene (2);
		}


	}

	IEnumerator sleep() {
		yield return new WaitForSeconds (50000);
		succeed = true;
	}

	void OnDisable() {
		s_tcp.closeSocket ();
	}
}





