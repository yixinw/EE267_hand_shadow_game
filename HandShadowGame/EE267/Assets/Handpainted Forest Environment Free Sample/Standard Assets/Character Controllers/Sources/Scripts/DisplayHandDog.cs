using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

using System;
using System.IO;
using System.Net.Sockets;
using System.Text;

public class DisplayHandDog : MonoBehaviour {

	private GameObject congrats;
	private bool succeed = false;
	private int current_score = -1;
	private int counter_text = 0;
	private string score = "";
	private int success_counter = -1;

	public Text scoreboard;
	private float rChannel = 0.0f;
	private int counter = 0;
	s_TCP s_tcp = new s_TCP();

	// Use this for initialization
	void Start () {
		// GetComponent<Renderer>().material.color = new Color(rChannel, 0.0f, 0.0f);
		s_tcp.setupSocket ();
		scoreboard.text = "Score N/A";
		congrats = GameObject.Find ("Congrats");
		congrats.SetActive (false);
	}

	// Update is called once per frame
	void Update () {
		counter += 1;
		if (counter > 5) {
			// add 3 after Hello, World! to tell server which shadow to load
			s_tcp.writeSocket ("Hello, World!3");
			byte[] buffer = s_tcp.readSocket ();
			if (buffer != null && buffer.Length > 0) {
				Debug.Log ("Received:" + Encoding.ASCII.GetString (buffer, 0, 5));
				// Create a texture. Texture size does not matter, since
				// LoadImage will replace with with incoming image size.
				if (buffer.Length < 10) {
					Debug.Log ("Succeed");
					current_score = 100;
					succeed = true;
					congrats.SetActive (true);
					success_counter = counter_text;
					// SceneManager.LoadScene (5);
				} else {
					Texture2D tex = new Texture2D (2, 2);
					byte[] score_buf = new byte[2];
					byte[] img_buf = new byte[buffer.Length - 2];
					Buffer.BlockCopy(buffer, 0, score_buf, 0, 2);
					Buffer.BlockCopy(buffer, 2, img_buf, 0, img_buf.Length);
					tex.LoadImage (img_buf);
					GetComponent<Renderer> ().material.SetTexture ("_MainTex", tex);
					score = System.Text.Encoding.UTF8.GetString(score_buf);
					scoreboard.text = "Score " + score;
					current_score = Int32.Parse(score);
					// scoreboard.text = "Score " + System.Text.Encoding.UTF8.GetString(score_buf);
					// tex.LoadImage (buffer);
					// GetComponent<Renderer> ().material.SetTexture ("_MainTex", tex);
				}
			} else {
				//Debug.Log ("Received nothing.");
			}
			counter = 0;
		}

		counter_text += 1;

		// hit space to move to the next scene
		// or wait for around a second to jump to the next level
		// if user succeeds
		if (counter_text > success_counter + 50 && succeed || Input.GetKeyDown ("space")) {
			SceneManager.LoadScene (4);
		}

	}

	void OnDisable() {
		s_tcp.closeSocket ();
	}
}

